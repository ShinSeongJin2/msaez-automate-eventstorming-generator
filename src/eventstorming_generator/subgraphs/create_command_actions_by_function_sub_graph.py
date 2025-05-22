import os
from typing import Callable, Dict, Any, List
from langgraph.graph import StateGraph

from ..models import ActionModel, CommandActionGenerationState, State, ESValueSummaryGeneratorModel
from ..generators import CreateCommandActionsByFunction
from ..utils import ESFakeActionsUtil, JsonUtil, ESValueSummarizeWithFilter, EsAliasTransManager, EsActionsUtil
from .es_value_summary_generator_sub_graph import create_es_value_summary_generator_subgraph

def prepare_command_actions_generation(state: State) -> State:
    """
    Command 액션 생성을 위한 초기 준비 작업 수행
    - 처리할 애그리거트 목록을 구성하고 상태 초기화
    """
    # 입력값이 있는지 확인
    if not state.inputs.selectedDraftOptions:
        state.subgraphs.createCommandActionsByFunctionModel.is_failed = True
        return state
    
    # 처리할 애그리거트 목록 초기화
    pending_generations = []
    
    # 각 BoundedContext와 Aggregate에 대한 생성 작업 준비
    for bc_name, draft_option in state.inputs.selectedDraftOptions.items():
        bounded_context = draft_option.get("boundedContext", {})
        
        # 현재 ES Value에서 해당 BoundedContext에 속한 Aggregate들을 찾음
        for element in state.outputs.esValue.elements.values():
            if (element and element.get("_type") == "org.uengine.modeling.model.Aggregate" and 
                element.get("boundedContext", {}).get("id") == bounded_context.get("id")):
                
                # 각 Aggregate에 대한 생성 상태 준비
                generation_state = CommandActionGenerationState(
                    target_bounded_context=bounded_context,
                    target_aggregate=element,
                    description=draft_option.get("description", ""),
                )
                pending_generations.append(generation_state)
    
    # 상태 업데이트
    state.subgraphs.createCommandActionsByFunctionModel.pending_generations = pending_generations
    state.subgraphs.createCommandActionsByFunctionModel.is_processing = True
    state.subgraphs.createCommandActionsByFunctionModel.all_complete = len(pending_generations) == 0
    
    return state

def select_next_command_actions(state: State) -> State:
    """
    다음에 처리할 Aggregate를 선택하는 노드
    """
    model = state.subgraphs.createCommandActionsByFunctionModel
    
    # 대기 중인 작업이 없으면 모든 작업 완료
    if len(model.pending_generations) == 0:
        model.all_complete = True
        model.is_processing = False
        return state
    
    # 다음 처리할 아이템 선택
    model.current_generation = model.pending_generations.pop(0)
    return state

def preprocess_command_actions_generation(state: State) -> State:
    """
    Command 액션 생성 전 전처리 작업 수행
    - 요약된 ES Value 생성
    - 요약된 정보가 토큰 제한을 초과하는지 확인하고 필요시 추가 요약
    """
    model = state.subgraphs.createCommandActionsByFunctionModel
    current = model.current_generation
    
    # 요약된 ES Value 생성을 위한 처리
    es_alias_trans_manager = EsAliasTransManager(state.outputs.esValue.model_dump())
    current.es_alias_trans_manager = es_alias_trans_manager
    
    # 요약된 ES Value 생성
    summarized_es_value = ESValueSummarizeWithFilter.get_summarized_es_value(
        state.outputs.esValue.model_dump(), [], es_alias_trans_manager
    )
    current.summarized_es_value = summarized_es_value
    
    # 여기서 토큰 제한 확인 로직이 필요한 경우 추가 구현
    # JS 코드에서는 토큰 제한 확인 후 추가 요약을 하는 부분이 있음
    # Python에서는 단순화하여 구현
    
    return state

def generate_command_actions(state: State) -> State:
    """
    지정된 Aggregate에 대한 Command 액션 생성 실행
    """
    model = state.subgraphs.createCommandActionsByFunctionModel
    current = model.current_generation
    
    try:
        # 요약 서브그래프에서 처리 결과를 받아온 경우
        if (hasattr(state.subgraphs.esValueSummaryGeneratorModel, 'is_complete') and 
            state.subgraphs.esValueSummaryGeneratorModel.is_complete and 
            state.subgraphs.esValueSummaryGeneratorModel.processed_summarized_es_value):
            
            # 요약된 결과로 상태 업데이트
            current.summarized_es_value = state.subgraphs.esValueSummaryGeneratorModel.processed_summarized_es_value
            
            # 요약 상태 초기화
            state.subgraphs.esValueSummaryGeneratorModel = ESValueSummaryGeneratorModel()
            
            current.is_token_over_limit = False
    
        # 모델명 가져오기
        model_name = os.getenv("AI_MODEL") or f"{state.inputs.llmModel.model_vendor}:{state.inputs.llmModel.model_name}"
        
        # Generator 초기화 및 실행
        generator = CreateCommandActionsByFunction(
            model_name=model_name,
            client={
                "inputs": {
                    "summarizedESValue": current.summarized_es_value,
                    "targetBoundedContext": current.target_bounded_context,
                    "targetAggregate": current.target_aggregate,
                    "description": current.description,
                    "esAliasTransManager": current.es_alias_trans_manager
                },
                "preferredLanguage": state.inputs.preferedLanguage
            }
        )
        
        # 토큰 수 계산 및 제한 확인
        token_count = generator.get_token_count()
        model_max_input_limit = state.inputs.llmModel.model_max_input_limit
        
        if token_count > model_max_input_limit:  # 토큰 제한 초과시 요약 처리
            # 축소된 요약 없이 필수 부분만으로 토큰 계산
            left_generator = CreateCommandActionsByFunction(
                model_name=model_name,
                client={
                    "inputs": {
                        "summarizedESValue": {},
                        "targetBoundedContext": current.target_bounded_context,
                        "targetAggregate": current.target_aggregate,
                        "description": current.description,
                        "esAliasTransManager": current.es_alias_trans_manager
                    },
                    "preferredLanguage": state.inputs.preferedLanguage
                }
            )
            
            # 남은 토큰 계산
            left_token_count = model_max_input_limit - left_generator.get_token_count()
            if left_token_count < 50:
                state.subgraphs.createCommandActionsByFunctionModel.is_failed = True
                return state
            
            # ES 요약 생성 서브그래프 호출 준비
            # 요약 생성 모델 초기화
            state.subgraphs.esValueSummaryGeneratorModel = ESValueSummaryGeneratorModel(
                is_processing=False,
                is_complete=False,
                context=_build_request_context(current),
                es_value=state.outputs.esValue.model_dump(),
                keys_to_filter=[],
                max_tokens=left_token_count,
                token_calc_model_vendor=state.inputs.llmModel.model_vendor,
                token_calc_model_name=state.inputs.llmModel.model_name
            )
            
            # 토큰 초과시 요약 서브그래프 호출하고 현재 상태 반환
            current.is_token_over_limit = True
            return state
        
        # Generator 실행
        result = generator.generate()
        result = JsonUtil.convert_to_dict(result)
        
        # 생성 결과가 있는지 확인
        if not result or not result.get("result"):
            # 실패 시 재시도 카운트 증가
            current.retry_count += 1
            return state
        
        # 생성된 액션 추출
        actions = []
        if "commandActions" in result["result"]:
            actions.extend(result["result"]["commandActions"])
        if "eventActions" in result["result"]:
            actions.extend(result["result"]["eventActions"])
        if "readModelActions" in result["result"]:
            actions.extend(result["result"]["readModelActions"])
        
        # 액션 객체 변환
        actionModels = [ActionModel(**action) for action in actions]
        for action in actionModels:
            action.type = "create"
        
        current.created_actions = actionModels
    except Exception as e:
        print(f"Command 액션 생성 오류: {e}")
        current.retry_count += 1
    
    return state

def postprocess_command_actions_generation(state: State) -> State:
    """
    생성된 Command 액션 후처리
    - 유효한 액션만 필터링
    - 필요한 변환 작업 수행
    - UUID 변환 등
    """
    model = state.subgraphs.createCommandActionsByFunctionModel
    current = model.current_generation
    
    try :
        # 유효한 액션만 필터링
        actions = filter_valid_actions(current.created_actions)
        
        # UUID 변환 처리
        if current.es_alias_trans_manager:
            actions = current.es_alias_trans_manager.trans_to_uuid_in_actions(actions)
        
        # 액션 복원 작업 (boundedContextId 추가 등)
        actions = restore_actions(actions, state.outputs.esValue.model_dump(), current.target_bounded_context.get("name", ""))
        
        # 기존 요소와 중복되는 액션 필터링
        actions = filter_actions(actions, state.outputs.esValue.model_dump())
        
        # Event의 outputCommandIds 속성 제거 (정책은 별도 처리)
        remove_event_output_command_ids(actions)
        
        # 부분 결과에 대한 가짜 액션 추가 (안정성을 위해)
        actions = ESFakeActionsUtil.add_fake_actions(actions, state.outputs.esValue)
        
        # 기본 속성 추가
        actions = add_default_properties(actions)
        
        # 처리된 액션 저장
        current.created_actions = actions


        # 생성된 액션을 ES Value에 적용
        user_info = state.inputs.userInfo.model_dump() if state.inputs.userInfo else {}
        information = state.inputs.information.model_dump() if state.inputs.information else {}
        
        updated_es_value = EsActionsUtil.apply_actions(
            state.outputs.esValue, 
            current.created_actions, 
            user_info, 
            information
        )
        
        # 상태 업데이트
        state.outputs.esValue = updated_es_value

        current.generation_complete = True
    except Exception as e:
        print(e)
        current.retry_count += 1
        current.created_actions = []
    
    return state

def validate_command_actions_generation(state: State) -> State:
    """
    Command 액션 생성 결과 검증 및 완료 처리
    - 생성 결과 검증
    - 완료 처리 또는 재시도 결정
    """
    # 현재 처리 중인 작업이 없으면 상태 유지
    if not state.subgraphs.createCommandActionsByFunctionModel.current_generation:
        return state
    
    current_gen = state.subgraphs.createCommandActionsByFunctionModel.current_generation
    
    # 생성 완료 확인
    if current_gen.generation_complete:
        # 완료된 작업을 완료 목록에 추가
        state.subgraphs.createCommandActionsByFunctionModel.completed_generations.append(current_gen)
        # 현재 작업 초기화
        state.subgraphs.createCommandActionsByFunctionModel.current_generation = None

    return state

def complete_processing(state: State) -> State:
    """
    모든 처리가 완료되면 최종 상태 업데이트
    """
    model = state.subgraphs.createCommandActionsByFunctionModel
    model.is_processing = False
    model.all_complete = True
    
    return state

def decide_next_step(state: State) -> str:
    """
    다음 단계 결정을 위한 라우팅 함수
    """
    # 모든 작업이 완료되었으면 완료 상태로 이동
    if state.subgraphs.createCommandActionsByFunctionModel.all_complete:
        return "complete"
    
    # 현재 처리 중인 작업이 없으면 다음 작업 선택
    if not state.subgraphs.createCommandActionsByFunctionModel.current_generation:
        return "select_next"
    
    current_gen = state.subgraphs.createCommandActionsByFunctionModel.current_generation
    if current_gen.retry_count > state.subgraphs.createCommandActionsByFunctionModel.max_retry_count:
        state.subgraphs.createCommandActionsByFunctionModel.is_failed = True
        return "complete"
    
    # 토큰 초과시 요약 서브그래프로 이동
    if current_gen.is_token_over_limit and hasattr(state.subgraphs.esValueSummaryGeneratorModel, 'is_complete'):
        if state.subgraphs.esValueSummaryGeneratorModel.is_complete:
            return "generate"
        else:
            return "es_value_summary_generator"

    # 현재 작업이 완료되었으면 검증 단계로 이동
    if current_gen.generation_complete:
        return "validate"
    
    # 전치리로 인한 요약 정보가 없을 경우, 전처리 단계로 이동
    if not current_gen.summarized_es_value:
        return "preprocess"
    
    # 기본적으로 생성 실행 단계로 이동
    if not current_gen.created_actions:
        return "generate"
    
    # 생성된 액션이 있으면 후처리 단계로 이동
    return "postprocess"

# 유틸리티 함수들
def filter_valid_actions(actions: List[ActionModel]) -> List[ActionModel]:
    """유효한 액션만 필터링"""
    # 기본 필터링 로직
    return [action for action in actions if 
            action.actionName and action.objectType and action.ids and action.ids.get("aggregateId")]

def restore_actions(actions: List[ActionModel], es_value: Dict[str, Any], target_bounded_context_name: str) -> List[ActionModel]:
    """액션 복원 처리"""
    # 타겟 BoundedContext 찾기
    target_bounded_context = None
    for element in es_value.get("elements", {}).values():
        if (element and element.get("_type") == "org.uengine.modeling.model.BoundedContext" and 
            element.get("name", "").lower() == target_bounded_context_name.lower()):
            target_bounded_context = element
            break
    
    if not target_bounded_context:
        raise ValueError(f"{target_bounded_context_name}에 대한 정보를 찾을 수 없습니다.")
    
    # 각 액션 복원
    for action in actions:
        if action.objectType == "Command":
            action.ids["boundedContextId"] = target_bounded_context.get("id")
            if not action.args:
                action.args = {}
            action.args["isRestRepository"] = False
        
        elif action.objectType == "Event":
            action.ids["boundedContextId"] = target_bounded_context.get("id")
            if not action.args:
                action.args = {}
        
        elif action.objectType == "ReadModel":
            action.ids["boundedContextId"] = target_bounded_context.get("id")
            if not action.args:
                action.args = {}
            action.args["properties"] = action.args.get("queryParameters", [])
    
    # Output Event/Command 관계 복원
    for action in actions:
        if action.objectType == "Command" and action.args and action.args.get("outputEventNames"):
            action.args["outputEventIds"] = [
                get_id_by_name(name, actions, es_value) 
                for name in action.args["outputEventNames"]
            ]
            action.args["outputEventIds"] = [id for id in action.args["outputEventIds"] if id]
        
        if action.objectType == "Event" and action.args and action.args.get("outputCommandNames"):
            action.args["outputCommandIds"] = [
                {
                    "commandId": get_id_by_name(name, actions, es_value),
                    "relatedAttribute": "",
                    "reason": ""
                }
                for name in action.args["outputCommandNames"]
            ]
            action.args["outputCommandIds"] = [cmd for cmd in action.args["outputCommandIds"] if cmd.get("commandId")]
    
    return actions

def get_id_by_name(name: str, actions: List[ActionModel], es_value: Dict[str, Any]) -> str:
    """이름으로 ID 찾기"""
    # 액션에서 찾기
    for action in actions:
        if (action.objectType == "Command" and action.args and 
            action.args.get("commandName") == name):
            return action.ids.get("commandId")
        if (action.objectType == "Event" and action.args and 
            action.args.get("eventName") == name):
            return action.ids.get("eventId")
    
    # ES Value에서 찾기
    for element in es_value.get("elements", {}).values():
        if element and element.get("name") == name and element.get("id"):
            return element.get("id")
    
    return None

def filter_actions(actions: List[ActionModel], es_value: Dict[str, Any]) -> List[ActionModel]:
    """중복 액션 필터링"""
    # 기존 요소 이름 목록
    es_names = [element.get("name") for element in es_value.get("elements", {}).values()
                if element and element.get("name")]
    
    display_names = [element.get("displayName").replace(" ", "") for element in es_value.get("elements", {}).values()
                    if element and element.get("displayName")]
    
    # 중복 및 검색/필터 관련 액션 제외
    filtered_actions = []
    for action in actions:
        if action.objectType == "Command":
            if (action.args.get("commandName") not in es_names and
                action.args.get("commandAlias").replace(" ", "") not in display_names and
                "search" not in action.args.get("commandName").lower() and
                "filter" not in action.args.get("commandName").lower()):
                filtered_actions.append(action)
        
        elif action.objectType == "Event":
            if (action.args.get("eventName") not in es_names and
                action.args.get("eventAlias").replace(" ", "") not in display_names and
                "search" not in action.args.get("eventName").lower() and
                "filter" not in action.args.get("eventName").lower()):
                filtered_actions.append(action)
        
        elif action.objectType == "ReadModel":
            if (action.args.get("readModelName") not in es_names and
                action.args.get("readModelAlias").replace(" ", "") not in display_names):
                filtered_actions.append(action)
    
    # 호출되지 않는 이벤트 제외
    output_event_ids = []
    for action in filtered_actions:
        if action.objectType == "Command" and action.args and action.args.get("outputEventIds"):
            output_event_ids.extend(action.args["outputEventIds"])
    
    return [action for action in filtered_actions if
            action.objectType != "Event" or action.ids.get("eventId") in output_event_ids]

def remove_event_output_command_ids(actions: List[ActionModel]) -> None:
    """Event의 outputCommandIds 속성 제거"""
    for action in actions:
        if action.objectType == "Event" and action.args and "outputCommandIds" in action.args:
            del action.args["outputCommandIds"]

def add_default_properties(actions: List[ActionModel]) -> List[ActionModel]:
    """기본 속성 추가"""
    # 여기서는 간단히 구현하고 필요시 확장
    return actions

def _build_request_context(current_gen) -> str:
    """
    요약 요청 컨텍스트 빌드
    """
    aggregate_name = current_gen.target_aggregate.get("name", "")
    aggregate_display_name = current_gen.target_aggregate.get("displayName", aggregate_name)
    bounded_context_name = current_gen.target_bounded_context.get("name", "")
    description = current_gen.description
    
    return f"""Creating commands, events, and read models for the following context:
- Target Bounded Context: {bounded_context_name}
- Target Aggregate: {aggregate_name}{ f" ({aggregate_display_name})" if aggregate_display_name and aggregate_display_name != aggregate_name else "" }
- Business Requirements
{description}

Focus on elements that are:
1. Directly related to the {aggregate_name} aggregate
2. Referenced by or dependent on the target aggregate
3. Essential for implementing the specified business requirements

This context is specifically for generating:
- Commands to handle business operations
- Events to record state changes
- Read models for query operations

All within the scope of {bounded_context_name} bounded context and {aggregate_name} aggregate."""

# 서브그래프 생성 함수
def create_command_actions_by_function_subgraph() -> Callable:
    """
    Command 액션 생성 서브그래프 생성
    """
    # 서브그래프 정의
    subgraph = StateGraph(State)
    
    # 노드 추가
    subgraph.add_node("prepare", prepare_command_actions_generation)
    subgraph.add_node("select_next", select_next_command_actions)
    subgraph.add_node("preprocess", preprocess_command_actions_generation)
    subgraph.add_node("generate", generate_command_actions)
    subgraph.add_node("postprocess", postprocess_command_actions_generation)
    subgraph.add_node("validate", validate_command_actions_generation)
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
            "generate": "generate",
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