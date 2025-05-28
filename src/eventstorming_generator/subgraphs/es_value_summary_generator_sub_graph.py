import os
from typing import Callable, Dict, Any, List
from copy import deepcopy
from langgraph.graph import StateGraph

from ..utils import JsonUtil, ESValueSummarizeWithFilter, TokenCounter, LogUtil, JobUtil
from ..models import State
from ..utils.es_alias_trans_manager import EsAliasTransManager
from ..generators.es_value_summary_generator import ESValueSummaryGenerator

# 노드 정의: ES 값 요약 생성 준비
def prepare_es_value_summary_generation(state: State) -> State:
    """
    ES 값 요약 생성을 위한 준비 작업 수행
    - 입력 데이터 설정 및 초기화
    """
    LogUtil.add_info_log(state, "ES 값 요약 생성 준비 시작...")
    
    try:
        # 이미 처리 중이거나 완료된 경우 상태 유지
        if state.subgraphs.esValueSummaryGeneratorModel.is_processing:
            LogUtil.add_info_log(state, "ES 값 요약 생성이 이미 처리 중입니다.")
            return state
        
        # 처리 상태 초기화
        state.subgraphs.esValueSummaryGeneratorModel.is_processing = True
        state.subgraphs.esValueSummaryGeneratorModel.is_complete = False
        state.subgraphs.esValueSummaryGeneratorModel.is_failed = False
        state.subgraphs.esValueSummaryGeneratorModel.retry_count = 0
        
        LogUtil.add_info_log(state, "ES 값 요약 생성 준비 완료")
        JobUtil.update_job_to_firebase_fire_and_forget(state)
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "ES 값 요약 생성 준비 중 오류 발생", e)
        state.subgraphs.esValueSummaryGeneratorModel.is_failed = True
        JobUtil.update_job_to_firebase_fire_and_forget(state)
    
    return state

# 노드 정의: ES 값 요약 생성 전처리
def preprocess_es_value_summary_generation(state: State) -> State:
    """
    ES 값 요약 생성을 위한 전처리 작업 수행
    - 요소 ID 추출
    - ES 별칭 변환 관리자 초기화
    """
    LogUtil.add_info_log(state, "ES 값 요약 전처리 시작...")
    
    try:
        es_value = state.outputs.esValue.model_dump()
        
        # ES 별칭 변환 관리자 초기화
        es_alias_trans_manager = EsAliasTransManager(es_value)
        
        # 요약된 ES 값 생성 (기본 필터링)
        summarized_es_value = ESValueSummarizeWithFilter.get_summarized_es_value(
            es_value,
            state.subgraphs.esValueSummaryGeneratorModel.keys_to_filter,
            es_alias_trans_manager
        )
        
        # 모든 요소 ID 추출
        element_ids = []
        
        def extract_ids(obj):
            if not obj or not isinstance(obj, dict):
                return
            
            if "id" in obj:
                element_ids.append(obj["id"])
            
            for value in obj.values():
                if isinstance(value, dict):
                    extract_ids(value)
                elif isinstance(value, list):
                    for item in value:
                        extract_ids(item)
        
        extract_ids(summarized_es_value)
        
        # 중복 제거
        element_ids = list(set(element_ids))
        
        # 요약 생성 모델 상태 업데이트
        state.subgraphs.esValueSummaryGeneratorModel.summarized_es_value = summarized_es_value
        state.subgraphs.esValueSummaryGeneratorModel.element_ids = element_ids
        
        LogUtil.add_info_log(state, f"ES 값 요약 전처리 완료 - 추출된 요소 ID 수: {len(element_ids)}")
        JobUtil.update_job_to_firebase_fire_and_forget(state)
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, "ES 값 요약 전처리 중 오류 발생", e)
        state.subgraphs.esValueSummaryGeneratorModel.retry_count += 1
        JobUtil.update_job_to_firebase_fire_and_forget(state)
    
    return state

# 노드 정의: ES 값 요약 생성 실행
def generate_es_value_summary(state: State) -> State:
    """
    ES 값 요약 생성 실행
    - ESValueSummaryGenerator를 통한 요소 ID 정렬
    """
    LogUtil.add_info_log(state, "ES 값 요약 생성 실행 시작...")
    
    try:
        # 모델명 가져오기
        model_name = os.getenv("AI_MODEL") or f"{state.inputs.llmModel.model_vendor}:{state.inputs.llmModel.model_name}"
        current_gen = state.subgraphs.esValueSummaryGeneratorModel
        
        LogUtil.add_info_log(state, f"사용할 AI 모델: {model_name}")
        
        # 요약 생성 Generator 생성
        generator = ESValueSummaryGenerator(
            model_name=model_name,
            client={
                "inputs": {
                    "context": current_gen.context,
                    "elementIds": current_gen.element_ids
                },
                "preferredLanguage": state.inputs.preferedLanguage
            }
        )
        
        # Generator 실행 결과
        result_dict = generator.generate(current_gen.retry_count > 0)
        
        # 결과에서 정렬된 요소 ID 추출
        if result_dict and "result" in result_dict and "sortedElementIds" in result_dict["result"]:
            sorted_element_ids = result_dict["result"]["sortedElementIds"]
            current_gen.sorted_element_ids = sorted_element_ids
            LogUtil.add_info_log(state, f"ES 값 요약 생성 완료 - 정렬된 요소 ID 수: {len(sorted_element_ids)}")
        else:
            raise ValueError("정렬된 요소 ID를 찾을 수 없습니다.")
        
        JobUtil.update_job_to_firebase_fire_and_forget(state)
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, "ES 값 요약 생성 중 오류 발생", e)
        current_gen.retry_count += 1
        JobUtil.update_job_to_firebase_fire_and_forget(state)
    
    return state

# 노드 정의: ES 값 요약 생성 후처리
def postprocess_es_value_summary_generation(state: State) -> State:
    """
    ES 값 요약 생성 후처리 작업 수행
    - 정렬된 요소 ID를 기준으로 토큰 제한 내에서 요약된 ES 값 생성
    """
    LogUtil.add_info_log(state, "ES 값 요약 후처리 시작...")
    
    try:
        if not state.subgraphs.esValueSummaryGeneratorModel.sorted_element_ids:
            raise ValueError("정렬된 요소 ID가 없습니다.")
        
        # 요소별로 그룹화하고 우선순위를 다시 재조정
        sorted_element_ids = _resort_with_priority(
            state.subgraphs.esValueSummaryGeneratorModel.summarized_es_value,
            state.subgraphs.esValueSummaryGeneratorModel.sorted_element_ids
        )
        
        LogUtil.add_info_log(state, f"우선순위 재정렬 완료 - 요소 수: {len(sorted_element_ids)}")
        
        # 토큰 제한 내에서 요약된 ES 값 생성
        summarized_es_value = _get_summary_within_token_limit(
            state.subgraphs.esValueSummaryGeneratorModel.summarized_es_value,
            sorted_element_ids,
            state.subgraphs.esValueSummaryGeneratorModel.max_tokens,
            state.subgraphs.esValueSummaryGeneratorModel.token_calc_model_vendor,
            state.subgraphs.esValueSummaryGeneratorModel.token_calc_model_name
        )
        
        # 결과 저장
        state.subgraphs.esValueSummaryGeneratorModel.processed_summarized_es_value = summarized_es_value
        
        LogUtil.add_info_log(state, "ES 값 요약 후처리 완료")
        JobUtil.update_job_to_firebase_fire_and_forget(state)
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, "ES 값 요약 후처리 중 오류 발생", e)
        state.subgraphs.esValueSummaryGeneratorModel.retry_count += 1
        JobUtil.update_job_to_firebase_fire_and_forget(state)
    
    return state

# 노드 정의: ES 값 요약 생성 검증
def validate_es_value_summary_generation(state: State) -> State:
    """
    ES 값 요약 생성 결과 검증
    - 생성된 요약 값 확인 및 완료 처리
    """
    LogUtil.add_info_log(state, "ES 값 요약 생성 검증 시작...")
    
    try:
        # 생성된 요약 값이 있으면 완료 처리
        if state.subgraphs.esValueSummaryGeneratorModel.processed_summarized_es_value:
            state.subgraphs.esValueSummaryGeneratorModel.is_complete = True
            LogUtil.add_info_log(state, "ES 값 요약 생성 검증 완료 - 성공")
        else:
            state.subgraphs.esValueSummaryGeneratorModel.retry_count += 1
            LogUtil.add_info_log(state, f"ES 값 요약 생성 검증 실패 - 재시도 횟수: {state.subgraphs.esValueSummaryGeneratorModel.retry_count}")
        
        JobUtil.update_job_to_firebase_fire_and_forget(state)
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, "ES 값 요약 생성 검증 중 오류 발생", e)
        state.subgraphs.esValueSummaryGeneratorModel.retry_count += 1
        JobUtil.update_job_to_firebase_fire_and_forget(state)
    
    return state

# 노드 정의: 완료 처리
def complete_processing(state: State) -> State:
    """
    ES 값 요약 생성 프로세스 완료
    """
    if state.subgraphs.esValueSummaryGeneratorModel.is_failed:
        LogUtil.add_info_log(state, "ES 값 요약 생성 프로세스 실패로 완료")
    else:
        LogUtil.add_info_log(state, "ES 값 요약 생성 프로세스 성공적으로 완료")
    
    try:
        
        state.subgraphs.esValueSummaryGeneratorModel.is_processing = False

        # 변수 정리
        subgraph_model = state.subgraphs.esValueSummaryGeneratorModel
        subgraph_model.context = ""
        subgraph_model.keys_to_filter = []
        subgraph_model.summarized_es_value = {}
        subgraph_model.element_ids = {}
        subgraph_model.sorted_element_ids = []

        JobUtil.update_job_to_firebase_fire_and_forget(state)
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, "ES 값 요약 생성 완료 처리 중 오류 발생", e)
    
    return state

# 라우팅 함수: 다음 단계 결정
def decide_next_step(state: State) -> str:
    """
    다음 실행할 단계 결정
    """
    if state.subgraphs.esValueSummaryGeneratorModel.is_failed:
        return "complete"

    # 완료된 경우 완료 상태로 이동
    if state.subgraphs.esValueSummaryGeneratorModel.is_complete:
        return "complete"
    
    # 재시도 횟수 초과시 실패 처리
    if state.subgraphs.esValueSummaryGeneratorModel.retry_count >= state.subgraphs.esValueSummaryGeneratorModel.max_retry_count:
        state.subgraphs.esValueSummaryGeneratorModel.is_failed = True
        state.subgraphs.esValueSummaryGeneratorModel.is_complete = True
        return "complete"
    
    # 요약된 ES 값이 없는 경우 전처리 단계로 이동
    if not state.subgraphs.esValueSummaryGeneratorModel.summarized_es_value:
        return "preprocess"
    
    # 정렬된 요소 ID가 없는 경우 생성 단계로 이동
    if not state.subgraphs.esValueSummaryGeneratorModel.sorted_element_ids:
        return "generate"
    
    # 요약된 결과가 없는 경우 후처리 단계로 이동
    if not state.subgraphs.esValueSummaryGeneratorModel.processed_summarized_es_value:
        return "postprocess"
    
    # 검증 단계로 이동
    return "validate"

# 서브그래프 생성 함수
def create_es_value_summary_generator_subgraph() -> Callable:
    """
    ES 값 요약 생성 서브그래프 생성
    """
    # 서브그래프 정의
    subgraph = StateGraph(State)
    
    # 노드 추가
    subgraph.add_node("prepare", prepare_es_value_summary_generation)
    subgraph.add_node("preprocess", preprocess_es_value_summary_generation)
    subgraph.add_node("generate", generate_es_value_summary)
    subgraph.add_node("postprocess", postprocess_es_value_summary_generation)
    subgraph.add_node("validate", validate_es_value_summary_generation)
    subgraph.add_node("complete", complete_processing)
    
    # 엣지 추가 (라우팅)
    subgraph.add_conditional_edges(
        "prepare",
        decide_next_step,
        {
            "preprocess": "preprocess",
            "complete": "complete"
        }
    )
    
    subgraph.add_conditional_edges(
        "preprocess",
        decide_next_step,
        {
            "generate": "generate",
            "complete": "complete"
        }
    )
    
    subgraph.add_conditional_edges(
        "generate",
        decide_next_step,
        {
            "postprocess": "postprocess",
            "validate": "validate",
            "complete": "complete"
        }
    )
    
    subgraph.add_conditional_edges(
        "postprocess",
        decide_next_step,
        {
            "validate": "validate",
            "generate": "generate",
            "complete": "complete"
        }
    )
    
    subgraph.add_conditional_edges(
        "validate",
        decide_next_step,
        {
            "preprocess": "preprocess",
            "complete": "complete"
        }
    )
    
    # 시작 및 종료 설정
    subgraph.set_entry_point("prepare")
    
    # 컴파일된 그래프 반환
    compiled_subgraph = subgraph.compile()
    
    # 서브그래프 실행 함수
    def run_subgraph(state: State) -> State:
        """
        서브그래프 실행 함수
        """
        # 서브그래프 실행
        result = State(**compiled_subgraph.invoke(state))
        return result
    
    return run_subgraph

# 유틸리티 함수: 우선순위 기반 요소 ID 재정렬
def _resort_with_priority(summarized_es_value: Dict[str, Any], sorted_element_ids: List[str]) -> List[str]:
    """
    그룹화 기반 우선순위 재정렬
    """
    bc_groups = {}
    non_bc_elements = set(sorted_element_ids)
    
    # 바운디드 컨텍스트별 그룹화
    for bc in summarized_es_value.get("boundedContexts", []):
        bc_id = bc.get("id")
        if not bc_id:
            continue
        
        bc_groups[bc_id] = {
            "bc": bc_id,
            "aggs": {},
            "originalOrder": sorted_element_ids.index(bc_id) if bc_id in sorted_element_ids else float('inf')
        }
        non_bc_elements.discard(bc_id)
        
        # 애그리게이트 그룹화
        for agg in bc.get("aggregates", []):
            agg_id = agg.get("id")
            if not agg_id:
                continue
            
            bc_groups[bc_id]["aggs"][agg_id] = {
                "agg": agg_id,
                "elements": [],
                "originalOrder": sorted_element_ids.index(agg_id) if agg_id in sorted_element_ids else float('inf')
            }
            non_bc_elements.discard(agg_id)
            
            # 애그리게이트 관련 요소 수집
            aggregate_elements = set()
            for type_key in ["valueObjects", "enumerations", "entities", "commands", "events", "readModels"]:
                for element in agg.get(type_key, []):
                    element_id = element.get("id")
                    if element_id:
                        aggregate_elements.add(element_id)
            
            # 정렬된 ID 목록에서 애그리게이트 관련 요소 선별
            for element_id in sorted_element_ids:
                if element_id in aggregate_elements:
                    bc_groups[bc_id]["aggs"][agg_id]["elements"].append(element_id)
                    non_bc_elements.discard(element_id)
    
    # 재정렬 결과 생성
    result = []
    
    # 바운디드 컨텍스트 기준 정렬
    for bc_group in sorted(bc_groups.values(), key=lambda x: x["originalOrder"]):
        result.append(bc_group["bc"])
        
        # 애그리게이트 기준 정렬
        for agg_group in sorted(bc_group["aggs"].values(), key=lambda x: x["originalOrder"]):
            result.append(agg_group["agg"])
            result.extend(agg_group["elements"])
    
    # 나머지 요소 추가
    for element_id in sorted_element_ids:
        if element_id in non_bc_elements:
            result.append(element_id)
    
    return result

# 유틸리티 함수: 토큰 제한 내에서 요약된 ES 값 생성
def _get_summary_within_token_limit(summarized_es_value: Dict[str, Any], sorted_element_ids: List[str], 
                                   max_tokens: int, token_calc_model_vendor: str, token_calc_model_name: str) -> Dict[str, Any]:
    """
    토큰 제한 내에서 요약된 ES 값 생성
    - 요소 우선순위에 따라 요약 수준 조정
    """
    element_ids = list(sorted_element_ids)
    left, right = 0, len(element_ids)
    result = None
    
    # 우선순위 기반 필터링 함수
    def filter_by_priority(obj, priority_index):
        if isinstance(obj, list):
            filtered = []
            for item in obj:
                # id 기반 우선순위 필터링
                if isinstance(item, dict) and "id" in item:
                    index = element_ids.index(item["id"]) if item["id"] in element_ids else float('inf')
                    if index < priority_index:
                        filtered.append(filter_by_priority(item, priority_index))
                else:
                    filtered.append(filter_by_priority(item, priority_index))
            
            # id 기반 정렬
            if filtered and isinstance(filtered[0], dict) and "id" in filtered[0]:
                filtered.sort(key=lambda x: element_ids.index(x["id"]) if x["id"] in element_ids else float('inf'))
            
            return filtered
        
        elif isinstance(obj, dict):
            filtered = {}
            for key, value in obj.items():
                filtered[key] = filter_by_priority(value, priority_index)
            return filtered
        
        return obj
    
    # 이진 탐색으로 최대 포함 가능한 요소 수 찾기
    while left <= right:
        mid = (left + right) // 2
        filtered = filter_by_priority(deepcopy(summarized_es_value), mid)
        json_string = JsonUtil.convert_to_json(filtered)
        
        token_count = TokenCounter.get_token_count(json_string, token_calc_model_vendor, token_calc_model_name)
        if token_count <= max_tokens:
            result = filtered
            left = mid + 1
        else:
            right = mid - 1
    
    if not result:
        raise ValueError("토큰 제한을 초과하여 요약할 수 없습니다.")
    
    return result
