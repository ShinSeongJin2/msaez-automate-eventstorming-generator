import time
import re
from typing import Callable, Dict, Any, List
from langgraph.graph import StateGraph, START

from ..models import ActionModel, CommandActionGenerationState, State, ESValueSummaryGeneratorModel
from ..utils import JsonUtil, ESValueSummarizeWithFilter, EsAliasTransManager, EsActionsUtil, LogUtil, JobUtil, EsTraceUtil
from ..generators import CreateCommandActionsByFunction, AssignEventNamesToAggregateDraft, AssignCommandViewNamesToAggregateDraft
from .es_value_summary_generator_sub_graph import create_es_value_summary_generator_subgraph
from ..constants import ResumeNodes
from ..config import Config


def resume_from_create_command_actions(state: State):
    try :
        
        state.subgraphs.createCommandActionsByFunctionModel.start_time = time.time()
        if state.outputs.lastCompletedRootGraphNode == ResumeNodes["ROOT_GRAPH"]["CREATE_COMMAND_ACTIONS"] and state.outputs.lastCompletedSubGraphNode:
            if state.outputs.lastCompletedSubGraphNode in ResumeNodes["CREATE_COMMAND_ACTIONS"].values():
                LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Resuming from checkpoint: '{state.outputs.lastCompletedSubGraphNode}'")
                return state.outputs.lastCompletedSubGraphNode
            else:
                state.subgraphs.createCommandActionsByFunctionModel.is_failed = True
                LogUtil.add_error_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Invalid checkpoint node: '{state.outputs.lastCompletedSubGraphNode}'")
                return "complete"
        
        LogUtil.add_info_log(state, "[COMMAND_ACTIONS_SUBGRAPH] Starting command actions generation process")
        return "prepare"
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[COMMAND_ACTIONS_SUBGRAPH] Failed during resume_from_create_command_actions", e)
        state.subgraphs.createCommandActionsByFunctionModel.is_failed = True
        return "complete"

def prepare_command_actions_generation(state: State) -> State:
    """
    Command 액션 생성을 위한 초기 준비 작업 수행
    - 처리할 애그리거트 목록을 구성하고 상태 초기화
    """
    
    try:

        LogUtil.add_info_log(state, "[COMMAND_ACTIONS_SUBGRAPH] Starting command actions generation preparation")

        # 입력값이 있는지 확인
        if not state.inputs.selectedDraftOptions:
            LogUtil.add_error_log(state, "[COMMAND_ACTIONS_SUBGRAPH] No selectedDraftOptions found in input data")
            state.subgraphs.createCommandActionsByFunctionModel.is_failed = True
            return state
        
        # 처리할 애그리거트 목록 초기화
        pending_generations = []
        total_aggregates = 0
        
        # 각 BoundedContext와 Aggregate에 대한 생성 작업 준비
        for bc_name, draft_option in state.inputs.selectedDraftOptions.items():
            bounded_context = draft_option.get("boundedContext", {})
            bc_display_name = bounded_context.get("displayName", bc_name)

            extractedElementNames = []
            try :
                siteMap = draft_option.get("boundedContext", None).get("requirements", None).get("siteMap", None)

                aggregateDraft = []
                for structure in draft_option.get("structure", []):
                    aggregateDraft.append(structure.get("aggregate", {}))
                
                if siteMap and aggregateDraft and len(aggregateDraft) > 0:
                    aiResponse = AssignCommandViewNamesToAggregateDraft(
                        model_name=Config.get_ai_model(),
                        client={
                            "inputs": {
                                "aggregateDrafts": aggregateDraft,
                                "siteMap": siteMap
                            }
                        }
                    ).generate()
                    extractedElementNames = aiResponse.get("result", {}).get("extractedCommands", []) + aiResponse.get("result", {}).get("extractedReadModels", [])
            except Exception as e:
                LogUtil.add_error_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Failed to extract element names for bounded context '{bc_name}':  {e}")

            # 현재 ES Value에서 해당 BoundedContext에 속한 Aggregate들을 찾음
            aggregates_in_bc = []
            for element in state.outputs.esValue.elements.values():
                if (element and element.get("_type") == "org.uengine.modeling.model.Aggregate" and 
                    element.get("boundedContext", {}).get("id") == bounded_context.get("id")):
                    aggregates_in_bc.append(element)

                    extractedElementNamesForAggregate = []
                    if extractedElementNames and len(extractedElementNames) > 0:
                        for extractedElementName in extractedElementNames:
                            if extractedElementName.get("aggregateName") == element.get("name", ""):
                                extractedElementNamesForAggregate.append(extractedElementName)
                    
                    # 각 Aggregate에 대한 생성 상태 준비
                    description = draft_option.get("description", "")
                    generation_state = CommandActionGenerationState(
                        target_bounded_context=bounded_context,
                        target_aggregate=element,
                        description=description,
                        original_description=description,
                        extractedElementNames=extractedElementNamesForAggregate
                    )
                    pending_generations.append(generation_state)
                    total_aggregates += 1
            
            LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Found {len(aggregates_in_bc)} aggregates in bounded context '{bc_display_name}': {[agg.get('name', 'Unknown') for agg in aggregates_in_bc]}")
        
        # 상태 업데이트
        state.subgraphs.createCommandActionsByFunctionModel.pending_generations = pending_generations
        state.subgraphs.createCommandActionsByFunctionModel.is_processing = True
        state.subgraphs.createCommandActionsByFunctionModel.all_complete = len(pending_generations) == 0
        
        LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Preparation completed. Total aggregates to process: {total_aggregates} across {len(state.inputs.selectedDraftOptions)} bounded contexts")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[COMMAND_ACTIONS_SUBGRAPH] Failed during command actions generation preparation", e)
        state.subgraphs.createCommandActionsByFunctionModel.is_failed = True
    
    return state

def assign_events_to_aggregates(state: State) -> State:
    """
    BC별 요청된 이벤트들을 해당 BC 내 적절한 애그리거트에 할당하는 노드
    """
    
    try:
        LogUtil.add_info_log(state, "[COMMAND_ACTIONS_SUBGRAPH] Starting event assignment to aggregates")
        
        model = state.subgraphs.createCommandActionsByFunctionModel
        
        # BC별로 이벤트 할당 처리
        for bc_name, draft_option in state.inputs.selectedDraftOptions.items():
            bounded_context = draft_option.get("boundedContext", {})
            bc_events = bounded_context.get("requirements", {}).get("event", [])
            
            if not bc_events:
                LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] No events to assign for bounded context '{bc_name}'")
                continue
                

            event_names = []
            try:
                event_names = re.findall(r'"name".*:.*"(.*?)"', bc_events)
                event_names = [name for name in event_names if name]    
            except Exception as e:
                LogUtil.add_error_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Failed to parse events for bounded context '{bc_name}': {e}")
                continue

            if not event_names:
                continue
            

            # 해당 BC의 애그리거트 목록 수집
            summarized_es_value = ESValueSummarizeWithFilter.get_summarized_es_value(
                state.outputs.esValue.model_dump(), [], EsAliasTransManager(state.outputs.esValue.model_dump())
            )

            aggregates_in_bc = []
            for bc in summarized_es_value.get("boundedContexts", []):
                if (bc and bc.get("name") != bc_name): continue

                for agg in bc.get("aggregates", []):
                    aggregate_info = {
                        "id": agg.get("id"),
                        "name": agg.get("name"),
                        "properties": []
                    }

                    for prop in agg.get("properties", []):
                        property_info = {
                            "name": prop.get("name"),
                            "type": prop.get("type") if prop.get("type") else "String"
                        }
                        if prop.get("isKey"):
                            property_info["isKey"] = True
                        aggregate_info["properties"].append(property_info)

                    aggregates_in_bc.append(aggregate_info)
                break
            
            if not aggregates_in_bc:
                LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] No aggregates found for bounded context '{bc_name}'")
                continue
            

            # 애그리거트가 1개인 경우 모든 이벤트를 해당 애그리거트에 할당
            if len(aggregates_in_bc) == 1:
                aggregate_name = aggregates_in_bc[0].get("name", "")
                LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Single aggregate '{aggregate_name}' found in BC '{bc_name}', assigning all {len(event_names)} events")
                
                # 해당 애그리거트의 generation state 찾아서 이벤트 할당
                for generation in model.pending_generations:
                    if (generation.target_aggregate.get("name") == aggregates_in_bc[0].get("name")):
                        generation.required_event_names = event_names
                        break
            else:
                # 애그리거트가 여러 개인 경우 LLM을 통해 이벤트 소속 결정
                LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Multiple aggregates found in BC '{bc_name}', using LLM to assign {len(event_names)} events to {len(aggregates_in_bc)} aggregates")
                
                # 모델명 가져오기
                model_name = Config.get_ai_model()
                
                # 이벤트 할당 생성기 실행
                assign_generator = AssignEventNamesToAggregateDraft(
                    model_name=model_name,
                    client={
                        "inputs": {
                            "boundedContextName": bounded_context.get("name", bc_name),
                            "aggregates": aggregates_in_bc,
                            "eventNames": event_names
                        },
                        "preferredLanguage": state.inputs.preferedLanguage
                    }
                )
                
                result = assign_generator.generate()
                
                if result and result.get("result"):
                    assignments = result["result"]
                    LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Event assignment completed for BC '{bc_name}': {len(assignments)} aggregates assigned")
                    
                    # 결과를 각 generation state에 할당
                    for assignment in assignments:
                        aggregate_name = assignment.get("aggregateName", "")
                        assigned_events = assignment.get("eventNames", [])
                        
                        # 해당 애그리거트의 generation state 찾기
                        for generation in model.pending_generations:
                            if generation.target_aggregate.get("name", "").lower() == aggregate_name.lower():
                                generation.required_event_names = assigned_events
                                LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Assigned {len(assigned_events)} events to aggregate '{aggregate_name}': {assigned_events}")
                                break
                else:
                    LogUtil.add_error_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Failed to get event assignment result for BC '{bc_name}'")
        
        LogUtil.add_info_log(state, "[COMMAND_ACTIONS_SUBGRAPH] Event assignment to aggregates completed")
        state.subgraphs.createCommandActionsByFunctionModel.assign_event_names_complete = True

    except Exception as e:
        LogUtil.add_exception_object_log(state, "[COMMAND_ACTIONS_SUBGRAPH] Failed during event assignment to aggregates", e)
        state.subgraphs.createCommandActionsByFunctionModel.is_failed = True
    
    return state

def select_next_command_actions(state: State) -> State:
    """
    다음에 처리할 Aggregate를 선택하는 노드
    """

    try:

        state.outputs.lastCompletedRootGraphNode = ResumeNodes["ROOT_GRAPH"]["CREATE_COMMAND_ACTIONS"]
        state.outputs.lastCompletedSubGraphNode = ResumeNodes["CREATE_COMMAND_ACTIONS"]["SELECT_NEXT"]
        JobUtil.update_job_to_firebase_fire_and_forget(state)

        model = state.subgraphs.createCommandActionsByFunctionModel
        pending_count = len(model.pending_generations)
        completed_count = len(model.completed_generations)
        
        LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Selecting next command actions generation. Pending: {pending_count}, Completed: {completed_count}")

        # 대기 중인 작업이 없으면 모든 작업 완료
        if len(model.pending_generations) == 0:
            model.all_complete = True
            model.is_processing = False
            LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] All command actions generations completed successfully. Total processed: {completed_count} aggregates")
            return state
        
        # 다음 처리할 아이템 선택
        model.current_generation = model.pending_generations.pop(0)
        
        aggregate_name = model.current_generation.target_aggregate.get("name", "Unknown")
        bc_name = model.current_generation.target_bounded_context.get("name", "Unknown")
        remaining_count = len(model.pending_generations)
        LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Selected next aggregate: '{aggregate_name}' in context '{bc_name}' (remaining: {remaining_count})")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[COMMAND_ACTIONS_SUBGRAPH] Failed to select next command actions generation", e)
        state.subgraphs.createCommandActionsByFunctionModel.is_failed = True
    
    return state

def preprocess_command_actions_generation(state: State) -> State:
    """
    Command 액션 생성 전 전처리 작업 수행
    - 요약된 ES Value 생성
    - 요약된 정보가 토큰 제한을 초과하는지 확인하고 필요시 추가 요약
    """
    model = state.subgraphs.createCommandActionsByFunctionModel
    current = model.current_generation
    
    if not current:
        LogUtil.add_info_log(state, "[COMMAND_ACTIONS_SUBGRAPH] No current generation found, skipping preprocessing")
        return state
        
    aggregate_name = current.target_aggregate.get("name", "Unknown")
    bc_name = current.target_bounded_context.get("name", "Unknown")
    LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Starting preprocessing for aggregate '{aggregate_name}' in context '{bc_name}'")
    
    try:

        # 기능 요구사항에 라인 번호 추가
        if current.description:
            current.description = EsTraceUtil.add_line_numbers_to_description(current.description)

        # 요약된 ES Value 생성
        summarized_es_value = ESValueSummarizeWithFilter.get_summarized_es_value(
            state.outputs.esValue.model_dump(), [], EsAliasTransManager(state.outputs.esValue.model_dump())
        )
        current.summarized_es_value = summarized_es_value
        
        LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Preprocessing completed for aggregate '{aggregate_name}'. Summary size: {len(str(summarized_es_value))} chars")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Preprocessing failed for aggregate '{aggregate_name}' in context '{bc_name}'", e)
        state.subgraphs.createCommandActionsByFunctionModel.is_failed = True
    
    return state

def generate_command_actions(state: State) -> State:
    """
    지정된 Aggregate에 대한 Command 액션 생성 실행
    """
    model = state.subgraphs.createCommandActionsByFunctionModel
    current_gen = model.current_generation
    
    if not current_gen:
        LogUtil.add_info_log(state, "[COMMAND_ACTIONS_SUBGRAPH] No current generation found, skipping generation")
        return state
        
    aggregate_name = current_gen.target_aggregate.get("name", "Unknown")
    bc_name = current_gen.target_bounded_context.get("name", "Unknown")
    retry_info = f" (retry {current_gen.retry_count})" if current_gen.retry_count > 0 else ""
    LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Generating command actions for aggregate '{aggregate_name}' in context '{bc_name}'{retry_info}")
    
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
            LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Applied summarized ES value for aggregate '{aggregate_name}' from summary generator")
    
        # 모델명 가져오기
        model_name = Config.get_ai_model()
        
        # Generator 초기화 및 실행
        generator = CreateCommandActionsByFunction(
            model_name=model_name,
            client={
                "inputs": {
                    "summarizedESValue": current_gen.summarized_es_value,
                    "description": current_gen.description,
                    "targetAggregate": current_gen.target_aggregate,
                    "requiredEventNames": current_gen.required_event_names,
                    "extractedElementNames": current_gen.extractedElementNames
                },
                "preferredLanguage": state.inputs.preferedLanguage
            }
        )
        
        # 토큰 수 계산 및 제한 확인
        token_count = generator.get_token_count()
        model_max_input_limit = Config.get_ai_model_max_input_limit()
        
        LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Token usage for aggregate '{aggregate_name}': {token_count}/{model_max_input_limit}")
        
        if token_count > model_max_input_limit:  # 토큰 제한 초과시 요약 처리
            LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Token limit exceeded for aggregate '{aggregate_name}' ({token_count} > {model_max_input_limit}), preparing summary generation")
            
            # 축소된 요약 없이 필수 부분만으로 토큰 계산
            left_generator = CreateCommandActionsByFunction(
                model_name=model_name,
                client={
                    "inputs": {
                        "summarizedESValue": {},
                        "description": current_gen.description,
                        "targetAggregate": current_gen.target_aggregate,
                        "requiredEventNames": current_gen.required_event_names,
                        "extractedElementNames": current_gen.extractedElementNames
                    },
                    "preferredLanguage": state.inputs.preferedLanguage
                }
            )
            
            # 남은 토큰 계산
            left_token_count = model_max_input_limit - left_generator.get_token_count()
            if left_token_count < 50:
                LogUtil.add_error_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Insufficient tokens remaining for aggregate '{aggregate_name}' generation")
                state.subgraphs.createCommandActionsByFunctionModel.is_failed = True
                return state
            
            # ES 요약 생성 서브그래프 호출 준비
            # 요약 생성 모델 초기화
            state.subgraphs.esValueSummaryGeneratorModel = ESValueSummaryGeneratorModel(
                is_processing=False,
                is_complete=False,
                context=_build_request_context(current_gen),
                keys_to_filter=[],
                max_tokens=left_token_count,
                token_calc_model_vendor=Config.get_ai_model_vendor(),
                token_calc_model_name=Config.get_ai_model_name()
            )
            
            # 토큰 초과시 요약 서브그래프 호출하고 현재 상태 반환
            current_gen.is_token_over_limit = True
            LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Prepared ES value summary request for aggregate '{aggregate_name}' (available tokens: {left_token_count})")
            return state
        
        # Generator 실행
        LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Executing command actions generation for aggregate '{aggregate_name}'")
        result = generator.generate(current_gen.retry_count > 0, current_gen.retry_count)
        
        # 생성 결과가 있는지 확인
        if not result or not result.get("result"):
            LogUtil.add_error_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] No valid result from command actions generation for aggregate '{aggregate_name}'")
            # 실패 시 재시도 카운트 증가
            current_gen.retry_count += 1
            return state
        
        # 생성된 액션 추출
        actions = []
        result_actions = result["result"]
        if "commandActions" in result_actions:
            actions.extend(result_actions["commandActions"])
        if "eventActions" in result_actions:
            actions.extend(result_actions["eventActions"])
        if "readModelActions" in result_actions:
            actions.extend(result_actions["readModelActions"])
        
        # 액션 객체 변환
        actionModels = [ActionModel(**action) for action in actions]
        for action in actionModels:
            action.type = "create"

            if action.objectType == "Command":
                for extractedElementName in current_gen.extractedElementNames:
                    if extractedElementName.get("commandName") == action.args.get("commandName"):
                        action.args["referencedSiteMapId"] = extractedElementName.get("referencedId")
                        break
            
            elif action.objectType == "ReadModel":
                for extractedElementName in current_gen.extractedElementNames:
                    if extractedElementName.get("readModelName") == action.args.get("readModelName"):
                        action.args["referencedSiteMapId"] = extractedElementName.get("referencedId")
                        break
        
        # 필수 이벤트 검증
        if current_gen.required_event_names:
            missing_events = validate_required_events(current_gen.required_event_names, actionModels)
            if missing_events:
                # 최대 재시도 횟수에 도달하지 않은 경우 재시도
                if current_gen.retry_count < state.subgraphs.createCommandActionsByFunctionModel.max_retry_count:
                    current_gen.retry_count += 1
                    LogUtil.add_error_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Missing required events for aggregate '{aggregate_name}': {missing_events}. Retrying generation (attempt {current_gen.retry_count})")
                    return state
                else:
                    # 최대 재시도 횟수에 도달한 경우 경고 로그만 출력하고 계속 진행
                    LogUtil.add_error_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Missing required events for aggregate '{aggregate_name}': {missing_events}. Maximum retry count reached, proceeding with current result")
        
        current_gen.created_actions = actionModels
        
        command_count = len(result_actions.get("commandActions", []))
        event_count = len(result_actions.get("eventActions", []))
        read_model_count = len(result_actions.get("readModelActions", []))
        LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Command actions generated successfully for aggregate '{aggregate_name}'. Commands: {command_count}, Events: {event_count}, ReadModels: {read_model_count}, Total: {len(actionModels)}")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Failed to generate command actions for aggregate '{aggregate_name}' in context '{bc_name}'", e)
        current_gen.retry_count += 1
    
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
    
    if not current:
        LogUtil.add_info_log(state, "[COMMAND_ACTIONS_SUBGRAPH] No current generation found, skipping postprocessing")
        return state
        
    aggregate_name = current.target_aggregate.get("name", "Unknown")
    bc_name = current.target_bounded_context.get("name", "Unknown")
    LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Starting postprocessing for aggregate '{aggregate_name}' in context '{bc_name}'")
    
    try:

        initial_action_count = len(current.created_actions)
        
        # Refs 후처리
        try:
            EsTraceUtil.convert_refs_to_indexes(current.created_actions, current.original_description, state, "[COMMAND_ACTIONS_SUBGRAPH]")
            LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Successfully converted source references for aggregate '{aggregate_name}'")
        except Exception as e:
            LogUtil.add_exception_object_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Failed to convert source references for aggregate '{aggregate_name}'", e)
            # 후처리 실패시에도 계속 진행하되, 에러 로그를 남김
        
        # 유효한 액션만 필터링
        actions = filter_valid_actions(current.created_actions)
        LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Filtered {initial_action_count} -> {len(actions)} valid actions for aggregate '{aggregate_name}'")
        
        # UUID 변환 처리
        actions = EsAliasTransManager(state.outputs.esValue.model_dump()).trans_to_uuid_in_actions(actions)
        
        # 액션 복원 작업 (boundedContextId 추가 등)
        actions = restore_actions(actions, state.outputs.esValue.model_dump(), current.target_bounded_context.get("name", ""))
        
        # 기존 요소와 중복되는 액션 필터링
        actions = filter_actions(actions, state.outputs.esValue.model_dump())
        LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Actions after duplicate filtering for aggregate '{aggregate_name}': {len(actions)}")
        
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
        
        LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Postprocessing completed successfully for aggregate '{aggregate_name}'. Final actions applied: {len(actions)}")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Postprocessing failed for aggregate '{aggregate_name}' in context '{bc_name}'", e)
        current.retry_count += 1
        current.created_actions = []
    
    return state

def validate_command_actions_generation(state: State) -> State:
    """
    Command 액션 생성 결과 검증 및 완료 처리
    - 생성 결과 검증
    - 완료 처리 또는 재시도 결정
    """
    current_gen = state.subgraphs.createCommandActionsByFunctionModel.current_generation
    if not current_gen:
        LogUtil.add_info_log(state, "[COMMAND_ACTIONS_SUBGRAPH] No current generation found, skipping validation")
        return state
        
    aggregate_name = current_gen.target_aggregate.get("name", "Unknown")
    bc_name = current_gen.target_bounded_context.get("name", "Unknown")
    LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Validating command actions generation for aggregate '{aggregate_name}' in context '{bc_name}'")
    
    try:

        # 생성 완료 확인
        if current_gen.generation_complete and not state.subgraphs.createCommandActionsByFunctionModel.is_failed:
            # 변수 정리
            current_gen.target_bounded_context = {}
            current_gen.target_aggregate = {}
            current_gen.description = ""
            current_gen.original_description = ""
            current_gen.summarized_es_value = {}
            current_gen.created_actions = []
            current_gen.required_event_names = []
            current_gen.extractedElementNames = []

            # 완료된 작업을 완료 목록에 추가
            state.subgraphs.createCommandActionsByFunctionModel.completed_generations.append(current_gen)
            # 현재 작업 초기화
            state.subgraphs.createCommandActionsByFunctionModel.current_generation = None
            state.outputs.currentProgressCount = state.outputs.currentProgressCount + 1
            
            total_progress = state.outputs.totalProgressCount
            current_progress = state.outputs.currentProgressCount
            LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Command actions generation validated and completed for aggregate '{aggregate_name}'. Progress: {current_progress}/{total_progress}")
        else:
            LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Command actions generation not yet complete for aggregate '{aggregate_name}', continuing process")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Validation failed for aggregate '{aggregate_name}' in context '{bc_name}'", e)
        state.subgraphs.createCommandActionsByFunctionModel.is_failed = True

    return state

def complete_processing(state: State) -> State:
    """
    모든 처리가 완료되면 최종 상태 업데이트
    """
    
    try:

        state.outputs.lastCompletedRootGraphNode = ResumeNodes["ROOT_GRAPH"]["CREATE_COMMAND_ACTIONS"]
        state.outputs.lastCompletedSubGraphNode = ResumeNodes["CREATE_COMMAND_ACTIONS"]["COMPLETE"]
        JobUtil.update_job_to_firebase_fire_and_forget(state)

        subgraph_model = state.subgraphs.createCommandActionsByFunctionModel
        subgraph_model.is_processing = False
        subgraph_model.all_complete = True
        
        completed_count = len(subgraph_model.completed_generations)
        failed = subgraph_model.is_failed
        if failed:
            LogUtil.add_error_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Command actions processing completed with failures. Successfully processed: {completed_count} aggregates")
        else:
            LogUtil.add_info_log(state, f"[COMMAND_ACTIONS_SUBGRAPH] Command actions processing completed successfully. Total processed: {completed_count} aggregates")

        if not failed:
            # 변수 정리
            subgraph_model.draft_options = {}
            subgraph_model.current_generation = None
            subgraph_model.completed_generations = []
            subgraph_model.pending_generations = []
        
        state.subgraphs.createCommandActionsByFunctionModel.end_time = time.time()
        state.subgraphs.createCommandActionsByFunctionModel.total_seconds = state.subgraphs.createCommandActionsByFunctionModel.end_time - state.subgraphs.createCommandActionsByFunctionModel.start_time
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[COMMAND_ACTIONS_SUBGRAPH] Failed during command actions processing completion", e)
        state.subgraphs.createCommandActionsByFunctionModel.is_failed = True
    
    return state

def decide_next_step(state: State) -> str:
    """
    다음 단계 결정을 위한 라우팅 함수
    """
    try :

        if state.subgraphs.createCommandActionsByFunctionModel.is_failed:
            return "complete"

        # 모든 작업이 완료되었으면 완료 상태로 이동
        if state.subgraphs.createCommandActionsByFunctionModel.all_complete:
            return "complete"
        
        # prepare 단계 직후라면 이벤트 할당 단계로 이동
        if not state.subgraphs.createCommandActionsByFunctionModel.assign_event_names_complete:
            return "assign_events"
        
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

    except Exception as e:
        LogUtil.add_exception_object_log(state, "[COMMAND_ACTIONS_SUBGRAPH] Failed during decide_next_step", e)
        state.subgraphs.createCommandActionsByFunctionModel.is_failed = True
        return "complete"

# 서브그래프 생성 함수
def create_command_actions_by_function_subgraph() -> Callable:
    """
    Command 액션 생성 서브그래프 생성
    """
    # 서브그래프 정의
    subgraph = StateGraph(State)
    
    # 노드 추가
    subgraph.add_node("prepare", prepare_command_actions_generation)
    subgraph.add_node("assign_events", assign_events_to_aggregates)
    subgraph.add_node("select_next", select_next_command_actions)
    subgraph.add_node("preprocess", preprocess_command_actions_generation)
    subgraph.add_node("generate", generate_command_actions)
    subgraph.add_node("postprocess", postprocess_command_actions_generation)
    subgraph.add_node("validate", validate_command_actions_generation)
    subgraph.add_node("complete", complete_processing)
    subgraph.add_node("es_value_summary_generator", create_es_value_summary_generator_subgraph())
    
    # 엣지 추가 (라우팅)
    subgraph.add_conditional_edges(START, resume_from_create_command_actions, {
        "prepare": "prepare",
        "assign_events": "assign_events",
        "select_next": "select_next",
        "preprocess": "preprocess",
        "generate": "generate",
        "postprocess": "postprocess",
        "validate": "validate",
        "complete": "complete",
        "es_value_summary_generator": "es_value_summary_generator"
    })

    subgraph.add_conditional_edges(
        "prepare",
        decide_next_step,
        {
            "assign_events": "assign_events",
            "complete": "complete"
        }
    )
    
    subgraph.add_conditional_edges(
        "assign_events",
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
            "generate": "generate",
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
    
    # 컴파일된 그래프 반환
    compiled_subgraph = subgraph.compile()
    
    # 서브그래프 실행 함수
    def run_subgraph(state: State) -> State:
        """
        서브그래프 실행 함수
        """
        # 서브그래프 실행
        result = State(**compiled_subgraph.invoke(state, {"recursion_limit": 2147483647}))
        return result
    
    return run_subgraph


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
    
    # 유효하지 않은 커맨드 액션 제거
    # 1. 모든 유효한 이벤트 ID 수집 (기존 es_value + 새로 생성된 action)
    all_event_ids = {
        element['id']
        for element in es_value.get("elements", {}).values()
        if element and element.get("_type") == "org.uengine.modeling.model.Event" and element.get('id')
    }
    all_event_ids.update({
        action.ids['eventId']
        for action in filtered_actions
        if action.objectType == "Event" and action.ids and action.ids.get('eventId')
    })

    # 2. Command의 outputEventIds를 검증하고, 유효한 이벤트가 없는 커맨드는 제거
    valid_commands_and_other_actions = []
    for action in filtered_actions:
        if action.objectType == "Command":
            if action.args and "outputEventIds" in action.args:
                valid_ids = [eid for eid in action.args.get("outputEventIds", []) if eid in all_event_ids]
                if valid_ids:
                    action.args["outputEventIds"] = valid_ids
                    valid_commands_and_other_actions.append(action)
                # else: 유효한 outputEventId가 하나도 없으면 커맨드 액션을 버립니다.
            else:
                # outputEventIds가 없는 커맨드는 그대로 유지합니다.
                valid_commands_and_other_actions.append(action)
        else:
            # Command가 아닌 다른 액션들은 그대로 유지합니다.
            valid_commands_and_other_actions.append(action)

    # 호출되지 않는 이벤트 제외
    output_event_ids = set()
    for action in valid_commands_and_other_actions:
        if action.objectType == "Command" and action.args and action.args.get("outputEventIds"):
            output_event_ids.update(action.args["outputEventIds"])
    
    return [
        action for action in valid_commands_and_other_actions
        if action.objectType != "Event" or (action.ids and action.ids.get("eventId") in output_event_ids)
    ]

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

def validate_required_events(required_event_names: List[str], action_models: List[ActionModel]) -> List[str]:
    """
    필수 이벤트가 생성된 액션에 포함되어 있는지 검증
    
    Args:
        required_event_names: 필수로 생성되어야 하는 이벤트 이름 목록
        action_models: 생성된 액션 모델 목록
    
    Returns:
        누락된 이벤트 이름 목록
    """
    # 생성된 이벤트 이름 목록 추출
    generated_event_names = set()
    for action in action_models:
        if action.objectType == "Event" and action.args and action.args["eventName"]:
            generated_event_names.add(action.args["eventName"])
    
    # 누락된 이벤트 찾기
    missing_events = [event_name for event_name in required_event_names 
                     if event_name not in generated_event_names]
    
    return missing_events
