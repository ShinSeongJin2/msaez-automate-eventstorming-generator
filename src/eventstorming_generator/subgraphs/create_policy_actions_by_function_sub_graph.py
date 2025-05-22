import os
from typing import Callable, Dict, Any, List
from copy import deepcopy
from langgraph.graph import StateGraph

from ..models import ActionModel, PolicyActionGenerationState, State, ESValueSummaryGeneratorModel
from ..generators import CreatePolicyActionsByFunction, ESValueSummaryGenerator
from ..utils import JsonUtil, ESValueSummarizeWithFilter, EsAliasTransManager, EsActionsUtil
from .es_value_summary_generator_sub_graph import create_es_value_summary_generator_subgraph

# 노드 정의: 초안으로부터 Policy 액션 생성 준비
def prepare_policy_actions_generation(state: State) -> State:
    """
    초안으로부터 Policy 액션 생성을 위한 준비 작업 수행
    - 초안 데이터 설정
    - 처리할 Policy 액션 목록 초기화
    """
    # 이미 처리 중이면 상태 유지
    if state.subgraphs.createPolicyActionsByFunctionModel.is_processing:
        return state
    
    # 초안 데이터 설정
    draft_options = state.inputs.selectedDraftOptions
    state.subgraphs.createPolicyActionsByFunctionModel.draft_options = draft_options
    state.subgraphs.createPolicyActionsByFunctionModel.is_processing = True
    state.subgraphs.createPolicyActionsByFunctionModel.all_complete = False
    state.subgraphs.createPolicyActionsByFunctionModel.completed_generations = []
    
    # 처리할 Policy 액션 목록 초기화
    pending_generations = []
    
    # 각 Bounded Context별로 처리할 Policy 액션 추출
    for bounded_context_name, bounded_context_data in draft_options.items():
        target_bounded_context = {"name": bounded_context_name}
        if "boundedContext" in bounded_context_data:
            target_bounded_context.update(bounded_context_data["boundedContext"])
        
        # Policy 액션 생성 상태 초기화
        generation_state = PolicyActionGenerationState(
            target_bounded_context=target_bounded_context,
            description=bounded_context_data.get("description", ""),
            retry_count=0,
            generation_complete=False
        )
        pending_generations.append(generation_state)
    
    # 처리할 Policy 액션 목록 저장
    state.subgraphs.createPolicyActionsByFunctionModel.pending_generations = pending_generations
    
    return state


# 노드 정의: 다음 생성할 Policy 액션 선택
def select_next_policy_actions(state: State) -> State:
    """
    다음에 생성할 Policy 액션을 선택하고 현재 처리 상태로 설정
    """
    # 모든 처리가 완료되었는지 확인
    if (not state.subgraphs.createPolicyActionsByFunctionModel.pending_generations and 
        not state.subgraphs.createPolicyActionsByFunctionModel.current_generation):
        state.subgraphs.createPolicyActionsByFunctionModel.all_complete = True
        state.subgraphs.createPolicyActionsByFunctionModel.is_processing = False
        return state
    
    # 현재 처리 중인 작업이 있으면 상태 유지
    if state.subgraphs.createPolicyActionsByFunctionModel.current_generation:
        return state
    
    # 대기 중인 Policy 액션이 있으면 첫 번째 항목을 현재 처리 상태로 설정
    if state.subgraphs.createPolicyActionsByFunctionModel.pending_generations:
        state.subgraphs.createPolicyActionsByFunctionModel.current_generation = state.subgraphs.createPolicyActionsByFunctionModel.pending_generations.pop(0)
    
    return state


# 노드 정의: Policy 액션 생성 전처리
def preprocess_policy_actions_generation(state: State) -> State:
    """
    Policy 액션 생성을 위한 전처리 작업 수행
    - 요약된 ES 값 생성
    - 별칭 변환 관리자 생성
    """
    # 현재 처리 중인 작업이 없으면 상태 유지
    if not state.subgraphs.createPolicyActionsByFunctionModel.current_generation:
        return state
    
    current_gen = state.subgraphs.createPolicyActionsByFunctionModel.current_generation
    
    # 현재 ES 값의 복사본 생성
    es_value = deepcopy(state.outputs.esValue.model_dump())
    
    # 별칭 변환 관리자 생성
    es_alias_trans_manager = EsAliasTransManager(es_value)
    current_gen.es_alias_trans_manager = es_alias_trans_manager
    
    # 요약된 ES 값 생성
    summarized_es_value = ESValueSummarizeWithFilter.get_summarized_es_value(
        es_value,
        ESValueSummarizeWithFilter.KEY_FILTER_TEMPLATES["aggregateInnerStickers"] + 
        ESValueSummarizeWithFilter.KEY_FILTER_TEMPLATES["detailedProperties"],
        es_alias_trans_manager
    )
    
    # 요약된 ES 값 저장
    current_gen.summarized_es_value = summarized_es_value
    
    return state


# 노드 정의: Policy 액션 생성 실행
def generate_policy_actions(state: State) -> State:
    """
    Policy 액션 생성 실행
    - Generator를 통한 Policy 액션 생성
    """
    # 현재 처리 중인 작업이 없으면 상태 유지
    if not state.subgraphs.createPolicyActionsByFunctionModel.current_generation:
        return state
    
    current_gen = state.subgraphs.createPolicyActionsByFunctionModel.current_generation
    
    try:
        # 요약 서브그래프에서 처리 결과를 받아온 경우
        if (hasattr(state.subgraphs.esValueSummaryGeneratorModel, 'is_complete') and 
            state.subgraphs.esValueSummaryGeneratorModel.is_complete and 
            state.subgraphs.esValueSummaryGeneratorModel.processed_summarized_es_value):
            
            # 요약된 결과로 상태 업데이트
            current_gen.summarized_es_value = state.subgraphs.esValueSummaryGeneratorModel.processed_summarized_es_value
            
            # 요약 상태 초기화
            state.subgraphs.esValueSummaryGeneratorModel = ESValueSummaryGeneratorModel()
            
            current_gen.is_token_over_limit = False

        # 모델명 가져오기
        model_name = os.getenv("AI_MODEL") or f"{state.inputs.llmModel.model_vendor}:{state.inputs.llmModel.model_name}"
        
        # Generator 생성
        generator = CreatePolicyActionsByFunction(
            model_name=model_name,
            client={
                "inputs": {
                    "summarizedESValue": current_gen.summarized_es_value,
                    "description": current_gen.description
                },
                "preferredLanguage": state.inputs.preferedLanguage
            }
        )
        
        # 토큰 초과 체크
        token_count = generator.get_token_count()
        model_max_input_limit = state.inputs.llmModel.model_max_input_limit
        
        if token_count > model_max_input_limit:  # 토큰 제한 초과시 요약 처리
            left_generator = CreatePolicyActionsByFunction(
                model_name=model_name,
                client={
                    "inputs": {
                        "summarizedESValue": {},
                        "description": current_gen.description
                    },
                    "preferredLanguage": state.inputs.preferedLanguage
                }
            )
            
            left_token_count = model_max_input_limit - left_generator.get_token_count()
            if left_token_count < 50:
                state.subgraphs.createPolicyActionsByFunctionModel.is_failed = True
                return state
            
            # ES 요약 생성 서브그래프 호출 준비
            # 요약 생성 모델 초기화
            state.subgraphs.esValueSummaryGeneratorModel = ESValueSummaryGeneratorModel(
                is_processing=False,
                is_complete=False,
                context=_build_request_context(current_gen),
                es_value=state.outputs.esValue.model_dump(),
                keys_to_filter=ESValueSummarizeWithFilter.KEY_FILTER_TEMPLATES["aggregateInnerStickers"] + 
                               ESValueSummarizeWithFilter.KEY_FILTER_TEMPLATES["detailedProperties"],
                max_tokens=left_token_count,
                token_calc_model_vendor=state.inputs.llmModel.model_vendor,
                token_calc_model_name=state.inputs.llmModel.model_name
            )
            
            # 토큰 초과시 요약 서브그래프 호출하고 현재 상태 반환
            current_gen.is_token_over_limit = True
            return state

        # Generator 실행 결과
        result = generator.generate()
        result = JsonUtil.convert_to_dict(result)
        
        # 결과에서 Policy 추출
        policies = []
        if result and "result" in result:
            policies = result["result"].get("extractedPolicies", [])
        
        # Policy를 액션으로 변환
        actions = _to_event_update_actions(
            policies, 
            current_gen.es_alias_trans_manager, 
            state.outputs.esValue.model_dump()
        )
        
        actionModels = [ActionModel(**action) for action in actions]
        
        # 생성된 액션 저장
        current_gen.created_actions = actionModels

        if len(current_gen.created_actions) == 0:
            current_gen.generation_complete = True
    
    except Exception as e:
        print(f"Error in generate_policy_actions: {e}")
        current_gen.retry_count += 1
    
    return state


# 노드 정의: Policy 액션 생성 후처리
def postprocess_policy_actions_generation(state: State) -> State:
    """
    Policy 액션 생성 후처리 작업 수행
    - 생성된 액션 적용
    - ES 값 업데이트
    """
    # 현재 처리 중인 작업이 없으면 상태 유지
    if not state.subgraphs.createPolicyActionsByFunctionModel.current_generation:
        return state
    
    current_gen = state.subgraphs.createPolicyActionsByFunctionModel.current_generation
    
    # 생성된 액션이 없으면 재시도 증가
    if not current_gen.created_actions:
        current_gen.retry_count += 1
        return state
    
    try:
        # ES 값의 복사본 생성
        es_value_to_modify = deepcopy(state.outputs.esValue)
        
        # 액션 적용하여 ES 값 업데이트
        updated_es_value = EsActionsUtil.apply_actions(
            es_value_to_modify,
            current_gen.created_actions,
            state.inputs.userInfo,
            state.inputs.information
        )
        
        # ES 값 업데이트
        state.outputs.esValue = updated_es_value
        current_gen.generation_complete = True
    
    except Exception as e:
        print(f"Error in postprocess_policy_actions_generation: {e}")
        current_gen.retry_count += 1
        current_gen.created_actions = []
    
    return state


# 노드 정의: Policy 액션 생성 검증 및 완료 처리
def validate_policy_actions_generation(state: State) -> State:
    """
    Policy 액션 생성 결과 검증 및 완료 처리
    - 생성 결과 검증
    - 완료 처리 또는 재시도 결정
    """
    # 현재 처리 중인 작업이 없으면 상태 유지
    if not state.subgraphs.createPolicyActionsByFunctionModel.current_generation:
        return state
    
    current_gen = state.subgraphs.createPolicyActionsByFunctionModel.current_generation
    
    # 생성 완료 확인
    if current_gen.generation_complete:
        # 완료된 작업을 완료 목록에 추가
        state.subgraphs.createPolicyActionsByFunctionModel.completed_generations.append(current_gen)
        # 현재 작업 초기화
        state.subgraphs.createPolicyActionsByFunctionModel.current_generation = None
    elif current_gen.retry_count >= state.subgraphs.createPolicyActionsByFunctionModel.max_retry_count:
        # 최대 재시도 횟수 초과 시 실패로 처리하고 다음 작업으로 이동
        state.subgraphs.createPolicyActionsByFunctionModel.completed_generations.append(current_gen)
        state.subgraphs.createPolicyActionsByFunctionModel.current_generation = None
    
    return state


# 단순 완료 처리를 위한 함수
def complete_processing(state: State) -> State:
    """
    Policy 액션 생성 프로세스 완료
    """
    return state


# 라우팅 함수: 다음 단계 결정
def decide_next_step(state: State) -> str:
    """
    다음 실행할 단계 결정
    """
    # 모든 작업이 완료되었으면 완료 상태로 이동
    if state.subgraphs.createPolicyActionsByFunctionModel.all_complete:
        return "complete"
    
    # 현재 처리 중인 작업이 없으면 다음 작업 선택
    if not state.subgraphs.createPolicyActionsByFunctionModel.current_generation:
        return "select_next"
    
    current_gen = state.subgraphs.createPolicyActionsByFunctionModel.current_generation
    
    # 최대 재시도 횟수 초과 시 검증 단계로 이동 (실패 처리)
    if current_gen.retry_count >= state.subgraphs.createPolicyActionsByFunctionModel.max_retry_count:
        return "validate"
    
    # 현재 작업이 완료되었으면 검증 단계로 이동
    if current_gen.generation_complete:
        return "validate"
    
    # 토큰 초과 상태 확인
    if current_gen.is_token_over_limit and hasattr(state.subgraphs.esValueSummaryGeneratorModel, 'is_complete'):
        if state.subgraphs.esValueSummaryGeneratorModel.is_complete:
            return "generate"
        else:
            return "es_value_summary_generator"
    
    # 전처리로 인한 요약 정보가 없을 경우, 전처리 단계로 이동
    if not current_gen.summarized_es_value:
        return "preprocess"
    
    # 기본적으로 생성 실행 단계로 이동
    if not current_gen.created_actions:
        return "generate"
    
    # 생성된 액션이 있으면 후처리 단계로 이동
    return "postprocess"


# 유틸리티 함수: 이벤트 업데이트 액션으로 변환
def _to_event_update_actions(policies: List[Dict[str, Any]], 
                           es_alias_trans_manager: Any, 
                           es_value: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    정책을 이벤트 업데이트 액션으로 변환
    """
    actions = []
    
    for policy in policies:
        # 이벤트 ID 획득
        event_id = es_alias_trans_manager.alias_to_uuid_dic.get(policy["fromEventId"])
        if not event_id:
            print(f"[!] Event ID not found for alias: {policy['fromEventId']}")
            continue
        
        # 이벤트 객체 획득
        event_object = es_value["elements"].get(event_id)
        if not event_object:
            print(f"[!] Event object not found for ID: {event_id}")
            continue
        
        # 커맨드 ID 획득
        command_id = es_alias_trans_manager.alias_to_uuid_dic.get(policy["toCommandId"])
        if not command_id:
            print(f"[!] Command ID not found for alias: {policy['toCommandId']}")
            continue
        
        # 커맨드 객체 획득
        command_object = es_value["elements"].get(command_id)
        if not command_object:
            print(f"[!] Command object not found for ID: {command_id}")
            continue
        
        # 이미 연결되어 있는지 확인
        is_already_connected = False
        target_policies = []
        
        # 이벤트에서 정책으로의 관계 찾기
        for relation in es_value["relations"].values():
            if not relation or not relation.get("sourceElement") or not relation.get("targetElement"):
                continue
            
            if (relation["sourceElement"].get("id") == event_object["id"] and 
                relation["targetElement"].get("_type") == "org.uengine.modeling.model.Policy"):
                target_policies.append(relation["targetElement"])
        
        # 정책에서 커맨드로의 관계 찾기
        if target_policies:
            for target_policy in target_policies:
                for relation in es_value["relations"].values():
                    if not relation or not relation.get("sourceElement") or not relation.get("targetElement"):
                        continue
                    
                    if (relation["sourceElement"].get("id") == target_policy["id"] and 
                        relation["targetElement"].get("id") == command_object["id"]):
                        is_already_connected = True
                        break
                
                if is_already_connected:
                    break
        
        # 이미 연결되어 있으면 스킵
        if is_already_connected:
            continue
        
        # 이벤트 업데이트 액션 생성
        actions.append({
            "objectType": "Event",
            "type": "update",
            "ids": {
                "boundedContextId": event_object["boundedContext"]["id"],
                "aggregateId": event_object["aggregate"]["id"],
                "eventId": event_object["id"]
            },
            "args": {
                "outputCommandIds": [{
                    "commandId": command_object["id"],
                    "reason": policy["reason"],
                    "name": policy["name"],
                    "alias": policy["alias"]
                }]
            }
        })
    
    return actions


# 요약 요청 컨텍스트 빌드 함수
def _build_request_context(current_gen) -> str:
    """
    요약 요청 컨텍스트 빌드
    """
    bounded_context_name = current_gen.target_bounded_context.get("name", "")
    bounded_context_display_name = current_gen.target_bounded_context.get("displayName", bounded_context_name)
    
    return f"""Task: Creating policies for {bounded_context_display_name} Bounded Context
    
Business Context:
{current_gen.description}

Focus:
- Events that should trigger commands in different aggregates or bounded contexts
- Business rules that require automatic reactions to system events
- Integration points between different parts of the domain
- Process flows that need automation through policies"""


# 서브그래프 생성 함수
def create_policy_actions_by_function_subgraph() -> Callable:
    """
    Policy 액션 생성 서브그래프 생성
    """
    # 서브그래프 정의
    subgraph = StateGraph(State)
    
    # 노드 추가
    subgraph.add_node("prepare", prepare_policy_actions_generation)
    subgraph.add_node("select_next", select_next_policy_actions)
    subgraph.add_node("preprocess", preprocess_policy_actions_generation)
    subgraph.add_node("generate", generate_policy_actions)
    subgraph.add_node("postprocess", postprocess_policy_actions_generation)
    subgraph.add_node("validate", validate_policy_actions_generation)
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
            "generate": "generate"
        }
    )
    
    subgraph.add_conditional_edges(
        "generate",
        decide_next_step,
        {
            "postprocess": "postprocess",
            "validate": "validate",
            "es_value_summary_generator": "es_value_summary_generator"
        }
    )
    
    subgraph.add_conditional_edges(
        "es_value_summary_generator",
        decide_next_step,
        {
            "generate": "generate"
        }
    )
    
    subgraph.add_conditional_edges(
        "postprocess",
        decide_next_step,
        {
            "validate": "validate"
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