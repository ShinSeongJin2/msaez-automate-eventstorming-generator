from typing import Dict, Any, List, Optional, Callable
from langgraph.graph import StateGraph
import os

from ..models import ClassIdGenerationState, State, ActionModel, ESValueSummaryGeneratorModel
from ..generators import CreateAggregateClassIdByDrafts
from ..utils import EsActionsUtil, ESValueSummarizeWithFilter, EsAliasTransManager, JsonUtil, EsUtils, CaseConvertUtil, LogUtil, JobUtil
from .es_value_summary_generator_sub_graph import create_es_value_summary_generator_subgraph


# 노드 정의: 클래스 ID 생성 준비
def prepare_class_id_generation(state: State) -> State:
    """
    Aggregate 클래스 ID 생성을 위한 준비 작업 수행
    - 초안 데이터 설정
    - 참조 관계 식별
    - 처리할 참조 목록 초기화
    """
    LogUtil.add_info_log(state, "Starting class ID generation preparation...")
    
    try:
        # 이미 처리 중이면 상태 유지
        if state.subgraphs.createAggregateClassIdByDraftsModel.is_processing:
            return state
        
        # 초안 데이터 설정
        draft_options = state.inputs.selectedDraftOptions
        draft_options = {k: v.get("structure", []) for k, v in draft_options.items()}

        state.subgraphs.createAggregateClassIdByDraftsModel.draft_options = draft_options
        state.subgraphs.createAggregateClassIdByDraftsModel.is_processing = True
        state.subgraphs.createAggregateClassIdByDraftsModel.all_complete = False
        
        # 참조 관계 추출
        references = []
        for bounded_context_id, bounded_context_data in draft_options.items():
            for structure in bounded_context_data:
                for vo in structure.get("valueObjects", []):
                    if "referencedAggregate" in vo:
                        references.append({
                            "fromAggregate": structure["aggregate"]["name"],
                            "toAggregate": vo["referencedAggregate"]["name"],
                            "referenceName": vo["name"]
                        })
        
        LogUtil.add_info_log(state, f"Found {len(references)} aggregate references")
        
        # 처리할 참조 목록 초기화
        if references:
            processed_pairs = set()
            pending_generations = []
            
            for ref in references:
                # 양방향 참조를 한 쌍으로 처리하기 위해 정렬된 키 생성
                pair_key = "-".join(sorted([ref["fromAggregate"], ref["toAggregate"]]))
                
                if pair_key not in processed_pairs:
                    processed_pairs.add(pair_key)
                    
                    # 양방향 참조 찾기
                    bidirectional_refs = [
                        r for r in references
                        if (r["fromAggregate"] == ref["fromAggregate"] and r["toAggregate"] == ref["toAggregate"]) or
                           (r["fromAggregate"] == ref["toAggregate"] and r["toAggregate"] == ref["fromAggregate"])
                    ]
                    
                    target_references = [r["referenceName"] for r in bidirectional_refs]
                    
                    # 생성 상태 객체 생성
                    generation_state = ClassIdGenerationState(
                        target_references=target_references,
                        draft_option=draft_options,
                        retry_count=0,
                        generation_complete=False
                    )
                    
                    pending_generations.append(generation_state)
            
            # 처리할 참조 목록 저장
            state.subgraphs.createAggregateClassIdByDraftsModel.pending_generations = pending_generations
            LogUtil.add_info_log(state, f"Prepared {len(pending_generations)} class ID generation tasks")
        else:
            LogUtil.add_info_log(state, "No aggregate references found")
        
        LogUtil.add_info_log(state, "Class ID generation preparation completed")
        JobUtil.update_job_to_firebase_fire_and_forget(state)
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"Error in class ID generation preparation", e)
        state.subgraphs.createAggregateClassIdByDraftsModel.is_failed = True
        JobUtil.update_job_to_firebase_fire_and_forget(state)
    
    return state


# 노드 정의: 다음 생성할 클래스 ID 선택
def select_next_class_id(state: State) -> State:
    """
    다음에 생성할 클래스 ID를 선택하고 현재 처리 상태로 설정
    """
    LogUtil.add_info_log(state, "Selecting next class ID generation task...")
    
    try:
        # 모든 처리가 완료되었는지 확인
        if (not state.subgraphs.createAggregateClassIdByDraftsModel.pending_generations and 
            not state.subgraphs.createAggregateClassIdByDraftsModel.current_generation):
            state.subgraphs.createAggregateClassIdByDraftsModel.all_complete = True
            state.subgraphs.createAggregateClassIdByDraftsModel.is_processing = False
            LogUtil.add_info_log(state, "All class ID generation tasks completed")
            return state
        
        # 현재 처리 중인 작업이 있으면 상태 유지
        if state.subgraphs.createAggregateClassIdByDraftsModel.current_generation:
            return state
        
        # 대기 중인 참조가 있으면 첫 번째 항목을 현재 처리 상태로 설정
        if state.subgraphs.createAggregateClassIdByDraftsModel.pending_generations:
            current_task = state.subgraphs.createAggregateClassIdByDraftsModel.pending_generations.pop(0)
            state.subgraphs.createAggregateClassIdByDraftsModel.current_generation = current_task
            
            LogUtil.add_info_log(state, f"Selected class ID generation task for references: {current_task.target_references}")
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"Error selecting next class ID task", e)
        state.subgraphs.createAggregateClassIdByDraftsModel.is_failed = True
    
    JobUtil.update_job_to_firebase_fire_and_forget(state)
    return state


# 노드 정의: 클래스 ID 생성 전처리
def preprocess_class_id_generation(state: State) -> State:
    """
    클래스 ID 생성을 위한 전처리 작업 수행
    - 요약된 ES 값 생성
    - ID 변환 처리
    """
    LogUtil.add_info_log(state, "Preprocessing class ID generation...")
    
    try:
        # 현재 처리 중인 작업이 없으면 상태 유지
        if not state.subgraphs.createAggregateClassIdByDraftsModel.current_generation:
            return state
        
        current_gen = state.subgraphs.createAggregateClassIdByDraftsModel.current_generation
        es_value = state.outputs.esValue.model_dump()        
  
        # 요약된 ES 값 생성
        current_gen.summarized_es_value = ESValueSummarizeWithFilter.get_summarized_es_value(
            es_value,
            ESValueSummarizeWithFilter.KEY_FILTER_TEMPLATES["aggregateOuterStickers"],
            EsAliasTransManager(es_value)
        )
        
        LogUtil.add_info_log(state, "Class ID generation preprocessing completed")
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"Error in class ID generation preprocessing", e)
        if state.subgraphs.createAggregateClassIdByDraftsModel.current_generation:
            state.subgraphs.createAggregateClassIdByDraftsModel.current_generation.retry_count += 1
    
    JobUtil.update_job_to_firebase_fire_and_forget(state)
    return state


# 노드 정의: 클래스 ID 생성 실행
def generate_class_id(state: State) -> State:
    """
    클래스 ID 생성 실행
    - Generator를 통한 클래스 ID 액션 생성
    - 토큰 초과 확인 및 요약 처리
    """
    LogUtil.add_info_log(state, "Generating class ID actions...")
    
    try:
        # 현재 처리 중인 작업이 없으면 상태 유지
        if not state.subgraphs.createAggregateClassIdByDraftsModel.current_generation:
            return state
        
        current_gen = state.subgraphs.createAggregateClassIdByDraftsModel.current_generation
        es_value = state.outputs.esValue.model_dump()
        
        # 요약 서브그래프에서 처리 결과를 받아온 경우
        if (hasattr(state.subgraphs.esValueSummaryGeneratorModel, 'is_complete') and 
            state.subgraphs.esValueSummaryGeneratorModel.is_complete and 
            state.subgraphs.esValueSummaryGeneratorModel.processed_summarized_es_value):
            
            LogUtil.add_info_log(state, "Using summarized ES value from summary generator")
            # 요약된 결과로 상태 업데이트
            current_gen.summarized_es_value = state.subgraphs.esValueSummaryGeneratorModel.processed_summarized_es_value
            
            # 요약 상태 초기화
            state.subgraphs.esValueSummaryGeneratorModel = ESValueSummaryGeneratorModel()

            current_gen.is_token_over_limit = False
        
        # 모델명 가져오기
        model_name = os.getenv("AI_MODEL") or f"{state.inputs.llmModel.model_vendor}:{state.inputs.llmModel.model_name}"
        
        # Generator 생성
        generator = CreateAggregateClassIdByDrafts(
            model_name=model_name,
            client={
                "inputs": {
                    "summarizedESValue": current_gen.summarized_es_value,
                    "draftOption": current_gen.draft_option,
                    "targetReferences": current_gen.target_references
                },
                "preferredLanguage": state.inputs.preferedLanguage
            }
        )
        
        # 토큰 초과 체크
        token_count = generator.get_token_count()
        model_max_input_limit = state.inputs.llmModel.model_max_input_limit
        
        LogUtil.add_info_log(state, f"Token count: {token_count}, Limit: {model_max_input_limit}")
        
        if token_count > model_max_input_limit:  # 토큰 제한 초과 시 요약 처리
            LogUtil.add_info_log(state, "Token limit exceeded, requesting ES value summary")
            
            left_generator = CreateAggregateClassIdByDrafts(
                model_name=model_name,
                client={
                    "inputs": {
                        "summarizedESValue": {},
                        "draftOption": current_gen.draft_option,
                        "targetReferences": current_gen.target_references
                    },
                    "preferredLanguage": state.inputs.preferedLanguage
                }
            )

            left_token_count = model_max_input_limit - left_generator.get_token_count()
            if left_token_count < 50:
                LogUtil.add_error_log(state, "Insufficient token space for class ID generation")
                state.subgraphs.createAggregateClassIdByDraftsModel.is_failed = True
                return state

            # ES 요약 생성 서브그래프 호출 준비
            # 요약 생성 모델 초기화
            state.subgraphs.esValueSummaryGeneratorModel = ESValueSummaryGeneratorModel(
                is_processing=False,
                is_complete=False,
                context=_build_request_context(current_gen),
                keys_to_filter=ESValueSummarizeWithFilter.KEY_FILTER_TEMPLATES["aggregateOuterStickers"],
                max_tokens=left_token_count,
                token_calc_model_vendor=state.inputs.llmModel.model_vendor,
                token_calc_model_name=state.inputs.llmModel.model_name
            )
            
            # 토큰 초과시 요약 서브그래프 호출하고 현재 상태 반환
            current_gen.is_token_over_limit = True
            return state
        
        # Generator 실행 결과
        LogUtil.add_info_log(state, f"Executing class ID generation for references: {current_gen.target_references}")
        result = generator.generate(current_gen.retry_count > 0)
        
        # 결과에서 액션 추출
        actions = []
        if result and "result" in result and "actions" in result["result"]:
            actions = result["result"]["actions"]
        
        LogUtil.add_info_log(state, f"Generated {len(actions)} initial actions")
        
        # 유효한 액션만 필터링
        filtered_actions = _filter_invalid_actions(actions, current_gen.target_references)
        filtered_actions = _filter_bidirectional_actions(filtered_actions, es_value, EsAliasTransManager(es_value))
        
        LogUtil.add_info_log(state, f"Filtered to {len(filtered_actions)} valid actions")
        
        actionModels = [ActionModel(**action) for action in filtered_actions]
        for action in actionModels:
            action.type = "create"

        # 생성된 액션 저장
        current_gen.created_actions = actionModels
        
        LogUtil.add_info_log(state, "Class ID generation completed successfully")
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"Error in class ID generation", e)
        if state.subgraphs.createAggregateClassIdByDraftsModel.current_generation:
            state.subgraphs.createAggregateClassIdByDraftsModel.current_generation.retry_count += 1
    
    JobUtil.update_job_to_firebase_fire_and_forget(state)
    return state


# 노드 정의: 클래스 ID 생성 후처리
def postprocess_class_id_generation(state: State) -> State:
    """
    클래스 ID 생성 후처리 작업 수행
    - 생성된 액션 검증
    - ID 변환
    - ES 값 업데이트
    """
    LogUtil.add_info_log(state, "Post-processing class ID generation...")
    
    try:
        # 현재 처리 중인 작업이 없으면 상태 유지
        if not state.subgraphs.createAggregateClassIdByDraftsModel.current_generation:
            return state
        
        current_gen = state.subgraphs.createAggregateClassIdByDraftsModel.current_generation
        es_value = state.outputs.esValue.model_dump()
        
        # 생성된 액션이 없으면 실패로 처리
        if not current_gen.created_actions:
            LogUtil.add_error_log(state, "No valid actions were created for class ID generation")
            current_gen.retry_count += 1
            return state
        
        LogUtil.add_info_log(state, f"Processing {len(current_gen.created_actions)} actions")
        
        # 액션 처리 및 적용
        actions = current_gen.created_actions
        actions = EsAliasTransManager(es_value).trans_to_uuid_in_actions(actions)
        actions = _modify_actions_for_reference_class_value_object(actions, es_value)
        
        # ES 값 업데이트
        updated_es_value = EsActionsUtil.apply_actions(
            es_value,
            actions,
            state.inputs.userInfo,
            state.inputs.information
        )
        
        # 상태 업데이트
        state.outputs.esValue = updated_es_value
        current_gen.generation_complete = True
        
        LogUtil.add_info_log(state, "Class ID generation post-processing completed successfully")

    except Exception as e:
        LogUtil.add_exception_object_log(state, f"Error in class ID generation post-processing", e)
        if state.subgraphs.createAggregateClassIdByDraftsModel.current_generation:
            current_gen = state.subgraphs.createAggregateClassIdByDraftsModel.current_generation
            current_gen.retry_count += 1
            current_gen.created_actions = []
    
    JobUtil.update_job_to_firebase_fire_and_forget(state)
    return state


# 노드 정의: 클래스 ID 생성 검증 및 완료 처리
def validate_class_id_generation(state: State) -> State:
    """
    클래스 ID 생성 결과 검증 및 완료 처리
    - 생성 결과 검증
    - 완료 처리 또는 재시도 결정
    """
    LogUtil.add_info_log(state, "Validating class ID generation...")
    
    try:
        # 현재 처리 중인 작업이 없으면 상태 유지
        if not state.subgraphs.createAggregateClassIdByDraftsModel.current_generation:
            return state
        
        current_gen = state.subgraphs.createAggregateClassIdByDraftsModel.current_generation
        
        # 생성 완료 확인
        if current_gen.generation_complete:
            LogUtil.add_info_log(state, f"Class ID generation completed for references: {current_gen.target_references}")

            # 변수 정리
            current_gen.target_references = []
            current_gen.draft_option = {}
            current_gen.summarized_es_value = {}
            current_gen.created_actions = []

            # 완료된 작업을 완료 목록에 추가
            state.subgraphs.createAggregateClassIdByDraftsModel.completed_generations.append(current_gen)
            # 현재 작업 초기화
            state.subgraphs.createAggregateClassIdByDraftsModel.current_generation = None
            state.outputs.currentProgressCount = state.outputs.currentProgressCount + 1

        elif current_gen.retry_count >= state.subgraphs.createAggregateClassIdByDraftsModel.max_retry_count:
            # 최대 재시도 횟수 초과 시 실패로 처리
            LogUtil.add_error_log(state, f"Max retry count exceeded for class ID generation: {current_gen.target_references}")
            state.subgraphs.createAggregateClassIdByDraftsModel.completed_generations.append(current_gen)
            state.subgraphs.createAggregateClassIdByDraftsModel.current_generation = None
            
        else:
            LogUtil.add_info_log(state, f"Retrying class ID generation (attempt {current_gen.retry_count + 1})")
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"Error in class ID generation validation", e)
        state.subgraphs.createAggregateClassIdByDraftsModel.is_failed = True
    
    JobUtil.update_job_to_firebase_fire_and_forget(state)
    return state


# 단순 완료 처리를 위한 함수
def complete_processing(state: State) -> State:
    """
    클래스 ID 생성 프로세스 완료
    """
    LogUtil.add_info_log(state, "Class ID generation process completed")
    JobUtil.update_job_to_firebase_fire_and_forget(state)

    # 변수 정리
    subgraph_model = state.subgraphs.createAggregateClassIdByDraftsModel
    subgraph_model.draft_options = {}
    subgraph_model.current_generation = None
    subgraph_model.completed_generations = []
    subgraph_model.pending_generations = []
    return state


# 라우팅 함수: 다음 단계 결정
def decide_next_step(state: State) -> str:
    """
    다음 실행할 단계 결정
    """
    # 작업 실패시에 강제로 완료 상태로 이동
    if state.subgraphs.createAggregateClassIdByDraftsModel.is_failed:
        return "complete"

    # 모든 작업이 완료되었으면 완료 상태로 이동
    if state.subgraphs.createAggregateClassIdByDraftsModel.all_complete:
        return "complete"
    
    # 현재 처리 중인 작업이 없으면 다음 작업 선택
    if not state.subgraphs.createAggregateClassIdByDraftsModel.current_generation:
        return "select_next"
    
    current_gen = state.subgraphs.createAggregateClassIdByDraftsModel.current_generation
    if current_gen.retry_count >= state.subgraphs.createAggregateClassIdByDraftsModel.max_retry_count:
        state.subgraphs.createAggregateClassIdByDraftsModel.is_failed = True
        return "validate"
    
    # 현재 작업이 완료되었으면 검증 단계로 이동
    if current_gen.generation_complete:
        return "validate"
    
    # 토큰 초과로 인한 요약이 필요한 경우 요약 서브그래프로 이동
    if current_gen.is_token_over_limit and hasattr(state.subgraphs.esValueSummaryGeneratorModel, 'is_complete'):
        if state.subgraphs.esValueSummaryGeneratorModel.is_complete:
            return "generate"
        else:
            return "es_value_summary_generator"
    
    # 전치리로 인한 요약 정보가 없을 경우, 전처리 단계로 이동
    if not current_gen.summarized_es_value:
        return "preprocess"
    
    # 기본적으로 생성 실행 단계로 이동
    if not current_gen.created_actions:
        return "generate"
    
    # 생성된 액션이 있으면 후처리 단계로 이동
    return "postprocess"


# 서브그래프 생성 함수
def create_aggregate_class_id_by_drafts_subgraph() -> Callable:
    """
    클래스 ID 생성 서브그래프 생성
    """
    # 서브그래프 정의
    subgraph = StateGraph(State)
    
    # 노드 추가
    subgraph.add_node("prepare", prepare_class_id_generation)
    subgraph.add_node("select_next", select_next_class_id)
    subgraph.add_node("preprocess", preprocess_class_id_generation)
    subgraph.add_node("generate", generate_class_id)
    subgraph.add_node("postprocess", postprocess_class_id_generation)
    subgraph.add_node("validate", validate_class_id_generation)
    subgraph.add_node("complete", complete_processing)
    subgraph.add_node("es_value_summary_generator", create_es_value_summary_generator_subgraph())
    
    # 엣지 추가 (라우팅)
    subgraph.add_conditional_edges(
        "prepare",
        decide_next_step,
        {
            "select_next": "select_next",
            "complete": "complete"
        }
    )
    
    subgraph.add_conditional_edges(
        "select_next",
        decide_next_step,
        {
            "select_next": "select_next",
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
            "es_value_summary_generator": "es_value_summary_generator",
            "complete": "complete"
        }
    )
    
    subgraph.add_conditional_edges(
        "es_value_summary_generator",
        decide_next_step,
        {
            "generate": "generate",
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
            "select_next": "select_next",
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


# 요약 요청 컨텍스트 빌드 함수
def _build_request_context(current_gen) -> str:
    """
    요약 요청 컨텍스트 빌드
    """
    # 관계 정보 추출
    relationships = []
    for bounded_context_id, bounded_context_data in current_gen.draft_option.items():
        for structure in bounded_context_data:
            if structure.get("valueObjects"):
                for vo in structure.get("valueObjects", []):
                    if vo.get("referencedAggregate"):
                        relationships.append({
                            "from": structure["aggregate"]["name"],
                            "to": vo["referencedAggregate"]["name"],
                            "reference": vo["name"]
                        })
    
    # 타겟 참조와 관련된 관계만 필터링
    relationship_descriptions = [
        f"{rel['from']} -> {rel['to']} (via {rel['reference']})"
        for rel in relationships
        if rel["reference"] in current_gen.target_references
    ]
    
    return f"""Analyzing aggregate relationships for creating ID Classes:
{chr(10).join(relationship_descriptions)}

Focus on elements related to these aggregates and their relationships, particularly for implementing the following references: {', '.join(current_gen.target_references)}.

Key considerations:
1. Aggregate relationships and their boundaries
2. Value objects that implement these relationships
3. Properties and identifiers needed for references
4. Related commands and events that might use these references"""


# 유틸리티 함수
def _filter_invalid_actions(actions: List[Dict[str, Any]], target_references: List[str]) -> List[Dict[str, Any]]:
    """
    유효하지 않은 액션 필터링
    """
    filtered_actions = []
    
    for action in actions:
        if not action.get("args") or not action["args"].get("valueObjectName"):
            continue
        
        if not action.get("ids") or not action["ids"].get("valueObjectId"):
            continue
        
        # 타겟 참조와 일치하는 액션만 유지
        is_valid_reference = any(
            target.lower() in action["args"]["valueObjectName"].lower()
            for target in target_references
        )
        
        if is_valid_reference:
            filtered_actions.append(action)
    
    return filtered_actions


def _filter_bidirectional_actions(actions: List[Dict[str, Any]], es_value: Dict[str, Any], es_alias_trans_manager: EsAliasTransManager) -> List[Dict[str, Any]]:
    """
    양방향 참조 액션 필터링 (한 방향만 유지)
    """
    for i in range(len(actions)):
        action1 = actions[i]
        if not action1:
            continue
        
        agg1_id = action1["ids"]["aggregateId"]
        agg1_element = es_value["elements"].get(es_alias_trans_manager.get_uuid_safely(agg1_id))
        if not agg1_element:
            continue
        
        agg1_name = agg1_element.get("name", "")
        
        for j in range(i + 1, len(actions)):
            action2 = actions[j]
            if not action2:
                continue
            
            agg2_id = action2["ids"]["aggregateId"]
            agg2_element = es_value["elements"].get(es_alias_trans_manager.get_uuid_safely(agg2_id))
            if not agg2_element:
                continue
            
            agg2_name = agg2_element.get("name", "")
            
            # 양방향 참조 확인
            if (action1["args"]["referenceClass"] == agg2_name and 
                action2["args"]["referenceClass"] == agg1_name):
                # 두 번째 액션 제거 (첫 번째 방향만 유지)
                actions[j] = None
    
    return [action for action in actions if action]


def _modify_actions_for_reference_class_value_object(actions: List[ActionModel], es_value: Dict[str, Any]) -> List[ActionModel]:
    """
    참조 클래스에 대한 액션 수정
    """
    actions_to_add = []
    
    for action in actions:
        if not action.args or not action.args["properties"]:
            continue
        
        # 참조할 Aggregate 찾기
        from_aggregate = _get_aggregate_by_id(es_value, action.ids["aggregateId"])
        to_aggregate = _get_aggregate_by_name(es_value, action.args["referenceClass"])
        
        if not from_aggregate or not to_aggregate:
            continue
        
        # 이름 형식 변경
        action.args["valueObjectName"] = f"{to_aggregate['name']}Id"
        
        # 키 속성 설정
        to_aggregate_key_prop = None
        if to_aggregate.get("aggregateRoot") and to_aggregate["aggregateRoot"].get("fieldDescriptors"):
            to_aggregate_key_prop = next(
                (prop for prop in to_aggregate["aggregateRoot"]["fieldDescriptors"] if prop.get("isKey")),
                None
            )
        
        if to_aggregate_key_prop:
            action_key_prop = next((prop for prop in action.args["properties"] if prop.get("isKey")), None)
            
            if action_key_prop:
                action_key_prop["name"] = to_aggregate_key_prop["name"]
                action_key_prop["type"] = to_aggregate_key_prop.get("className")
                action_key_prop["isKey"] = True
                action_key_prop["referenceClass"] = to_aggregate["name"]
                action_key_prop["isOverrideField"] = True
        
        # Aggregate 관계 추가
        _add_aggregate_relation(from_aggregate, to_aggregate, es_value)
        
        # 추가 액션 생성 (Aggregate 업데이트)
        actions_to_add.append(
            ActionModel(
                objectType="Aggregate",
                type="update",
                ids={
                    "boundedContextId": action.ids["boundedContextId"],
                    "aggregateId": action.ids["aggregateId"]
                },
                args={
                    "properties": [
                        {
                            "name": CaseConvertUtil.camel_case(action.args["valueObjectName"]),
                            "type": action.args["valueObjectName"],
                            "referenceClass": to_aggregate["name"],
                            "isOverrideField": True
                        }
                    ]
                }
            )
        )
    
    actions.extend(actions_to_add)
    return actions


def _get_aggregate_by_id(es_value: Dict[str, Any], aggregate_id: str) -> Optional[Dict[str, Any]]:
    """ID로 Aggregate 찾기"""
    aggregate = es_value["elements"].get(aggregate_id)
    if aggregate and aggregate.get("_type") == "org.uengine.modeling.model.Aggregate":
        return aggregate
    return None


def _get_aggregate_by_name(es_value: Dict[str, Any], aggregate_name: str) -> Optional[Dict[str, Any]]:
    """이름으로 Aggregate 찾기"""
    for element in es_value["elements"].values():
        if (element and 
            element.get("_type") == "org.uengine.modeling.model.Aggregate" and 
            element.get("name") == aggregate_name):
            return element
    return None


def _add_aggregate_relation(from_aggregate: Dict[str, Any], to_aggregate: Dict[str, Any], es_value: Dict[str, Any]) -> None:
    """Aggregate 간 관계 추가"""
    # 이미 관계가 있는지 확인
    for relation in es_value["relations"].values():
        if (relation and relation.get("sourceElement") and relation.get("targetElement") and
            relation["sourceElement"].get("id") == from_aggregate.get("id") and
            relation["targetElement"].get("id") == to_aggregate.get("id")):
            return
    
    # 관계 생성
    aggregate_relation = EsUtils.getEventStormingRelationObjectBase(from_aggregate, to_aggregate)
    es_value["relations"][aggregate_relation["id"]] = aggregate_relation
