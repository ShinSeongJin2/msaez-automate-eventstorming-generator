import os
from typing import Callable, Dict, Any, List
from copy import deepcopy
from langgraph.graph import StateGraph, START

from ..models import GWTGenerationState, State, ESValueSummaryGeneratorModel
from ..utils import ESValueSummarizeWithFilter, EsAliasTransManager, LogUtil, JobUtil
from ..generators import CreateGWTGeneratorByFunction
from .es_value_summary_generator_sub_graph import create_es_value_summary_generator_subgraph
from ..constants import ResumeNodes


def resume_from_create_gwt(state: State):
    try :

        if state.outputs.lastCompletedRootGraphNode == ResumeNodes["ROOT_GRAPH"]["CREATE_GWT"] and state.outputs.lastCompletedSubGraphNode:
            if state.outputs.lastCompletedSubGraphNode in ResumeNodes["CREATE_GWT"].values():
                LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Resuming from checkpoint: '{state.outputs.lastCompletedSubGraphNode}'")
                return state.outputs.lastCompletedSubGraphNode
            else:
                state.subgraphs.createGwtGeneratorByFunctionModel.is_failed = True
                LogUtil.add_error_log(state, f"[GWT_SUBGRAPH] Invalid checkpoint node: '{state.outputs.lastCompletedSubGraphNode}'")
                return "complete"
        
        LogUtil.add_info_log(state, "[GWT_SUBGRAPH] Starting GWT generation process")
        return "prepare"
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[GWT_SUBGRAPH] Failed during resume_from_create_gwt", e)
        state.subgraphs.createGwtGeneratorByFunctionModel.is_failed = True
        return "complete"

# 노드 정의: GWT 생성 준비
def prepare_gwt_generation(state: State) -> State:
    """
    GWT 생성을 위한 준비 작업 수행
    - 초안 데이터 설정
    - 처리할 Command 목록 초기화
    """
    
    try:

        LogUtil.add_info_log(state, "[GWT_SUBGRAPH] Starting GWT generation preparation")

        # 이미 처리 중이면 상태 유지
        if state.subgraphs.createGwtGeneratorByFunctionModel.is_processing:
            LogUtil.add_info_log(state, "[GWT_SUBGRAPH] GWT generation already in progress, maintaining state")
            return state
        
        # 초안 데이터 설정
        draft_options = state.inputs.selectedDraftOptions
        state.subgraphs.createGwtGeneratorByFunctionModel.draft_options = draft_options
        state.subgraphs.createGwtGeneratorByFunctionModel.is_processing = True
        state.subgraphs.createGwtGeneratorByFunctionModel.all_complete = False
        
        # 처리할 Command GWT 목록 초기화
        pending_generations = []
        total_aggregates = 0
        total_commands = 0
        
        # 각 Bounded Context별로 처리할 Aggregate 추출
        for bounded_context_name, bounded_context_data in draft_options.items():
            target_bounded_context = {"name": bounded_context_name}
            if "boundedContext" in bounded_context_data:
                target_bounded_context.update(bounded_context_data["boundedContext"])
            
            bc_display_name = target_bounded_context.get("displayName", bounded_context_name)
            
            # 해당 Bounded Context의 Aggregate들을 찾기
            es_value = deepcopy(state.outputs.esValue.model_dump())
            
            # Aggregate 각각에 대해 Command GWT 생성 준비
            target_aggregates = []
            for element in es_value.get("elements", {}).values():
                if element and element.get("_type") == "org.uengine.modeling.model.Aggregate" and \
                   element.get("boundedContext", {}).get("id") == target_bounded_context.get("id"):
                    target_aggregates.append(element)
            
            for target_aggregate in target_aggregates:
                # Aggregate에 연결된 Command 목록 찾기
                target_command_ids = []
                target_aggregate_name = target_aggregate.get("name", "Unknown")
                
                for element in es_value.get("elements", {}).values():
                    if element and element.get("_type") == "org.uengine.modeling.model.Command" and \
                       element.get("aggregate", {}).get("id") == target_aggregate.get("id"):
                        target_command_ids.append(element.get("id"))
                
                if not target_command_ids:
                    LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] No commands found for aggregate '{target_aggregate_name}' in context '{bc_display_name}', skipping")
                    continue  # Command가 없으면 처리하지 않음
                
                # 각 Aggregate의 Command들에 대한 GWT 생성 상태 초기화
                generation_state = GWTGenerationState(
                    target_bounded_context=target_bounded_context,
                    target_command_ids=target_command_ids,
                    target_aggregate_names=[target_aggregate_name],
                    description=bounded_context_data.get("description", ""),
                    retry_count=0,
                    generation_complete=False
                )
                pending_generations.append(generation_state)
                total_aggregates += 1
                total_commands += len(target_command_ids)
                LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Queued GWT generation for aggregate '{target_aggregate_name}' in context '{bc_display_name}' ({len(target_command_ids)} commands)")
        
        # 처리할 GWT 생성 목록 저장
        state.subgraphs.createGwtGeneratorByFunctionModel.pending_generations = pending_generations
        
        LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Preparation completed. Total tasks: {len(pending_generations)} ({total_aggregates} aggregates, {total_commands} commands)")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[GWT_SUBGRAPH] Failed during GWT generation preparation", e)
        state.subgraphs.createGwtGeneratorByFunctionModel.is_failed = True

    return state

# 노드 정의: 다음 생성할 GWT 선택
def select_next_gwt_generation(state: State) -> State:
    """
    다음에 생성할 GWT를 선택하고 현재 처리 상태로 설정
    """
    
    try:

        state.outputs.lastCompletedRootGraphNode = ResumeNodes["ROOT_GRAPH"]["CREATE_GWT"]
        state.outputs.lastCompletedSubGraphNode = ResumeNodes["CREATE_GWT"]["SELECT_NEXT"]
        JobUtil.update_job_to_firebase_fire_and_forget(state)

        pending_count = len(state.subgraphs.createGwtGeneratorByFunctionModel.pending_generations)
        completed_count = len(state.subgraphs.createGwtGeneratorByFunctionModel.completed_generations)
        
        LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Selecting next GWT generation task. Pending: {pending_count}, Completed: {completed_count}")

        # 모든 처리가 완료되었는지 확인
        if (not state.subgraphs.createGwtGeneratorByFunctionModel.pending_generations and 
            not state.subgraphs.createGwtGeneratorByFunctionModel.current_generation):
            state.subgraphs.createGwtGeneratorByFunctionModel.all_complete = True
            state.subgraphs.createGwtGeneratorByFunctionModel.is_processing = False
            LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] All GWT generation tasks completed successfully. Total processed: {completed_count} aggregate tasks")
            return state
        
        # 현재 처리 중인 작업이 있으면 상태 유지
        if state.subgraphs.createGwtGeneratorByFunctionModel.current_generation:
            current = state.subgraphs.createGwtGeneratorByFunctionModel.current_generation
            bc_name = current.target_bounded_context.get("displayName", current.target_bounded_context.get("name", "Unknown"))
            aggregate_names = ", ".join(current.target_aggregate_names)
            LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Current GWT generation in progress for aggregates '{aggregate_names}' in context '{bc_name}'")
            return state
        
        # 대기 중인 GWT 생성이 있으면 첫 번째 항목을 현재 처리 상태로 설정
        if state.subgraphs.createGwtGeneratorByFunctionModel.pending_generations:
            next_generation = state.subgraphs.createGwtGeneratorByFunctionModel.pending_generations.pop(0)
            state.subgraphs.createGwtGeneratorByFunctionModel.current_generation = next_generation
            
            bc_name = next_generation.target_bounded_context.get("displayName", next_generation.target_bounded_context.get("name", "Unknown"))
            aggregate_names = ", ".join(next_generation.target_aggregate_names)
            command_count = len(next_generation.target_command_ids)
            remaining_count = len(state.subgraphs.createGwtGeneratorByFunctionModel.pending_generations)
            LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Selected next GWT generation task for aggregates '{aggregate_names}' in context '{bc_name}' ({command_count} commands, remaining: {remaining_count})")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[GWT_SUBGRAPH] Failed to select next GWT generation task", e)
        state.subgraphs.createGwtGeneratorByFunctionModel.is_failed = True
    
    return state

# 노드 정의: GWT 생성 전처리
def preprocess_gwt_generation(state: State) -> State:
    """
    GWT 생성을 위한 전처리 작업 수행
    - ID 변환 매니저 생성
    - 요약된 ES 값 생성
    - 명령어 별칭 생성
    """
    current_gen = state.subgraphs.createGwtGeneratorByFunctionModel.current_generation
    if not current_gen:
        LogUtil.add_info_log(state, "[GWT_SUBGRAPH] No GWT generation task currently being processed, skipping preprocessing")
        return state
        
    bc_name = current_gen.target_bounded_context.get("displayName", current_gen.target_bounded_context.get("name", "Unknown"))
    aggregate_names = ", ".join(current_gen.target_aggregate_names)
    command_count = len(current_gen.target_command_ids)
    LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Starting preprocessing for aggregates '{aggregate_names}' in context '{bc_name}' ({command_count} commands)")
    
    try:

        # 현재 ES 값의 복사본 생성
        es_value = deepcopy(state.outputs.esValue.model_dump())
        
        # 별칭 변환 관리자 생성
        es_alias_trans_manager = EsAliasTransManager(es_value)
        
        # 명령어 별칭 생성
        current_gen.target_command_aliases = [
            es_alias_trans_manager.uuid_to_alias_dic.get(command_id, command_id)
            for command_id in current_gen.target_command_ids
        ]
        
        # 요약된 ES 값 생성
        summarized_es_value = {
            "deletedProperties": [],
            "boundedContexts": [
                ESValueSummarizeWithFilter.get_summarized_bounded_context_value(
                    es_value,
                    current_gen.target_bounded_context,
                    [],
                    es_alias_trans_manager
                )
            ]
        }
        
        # 요약된 ES 값 저장
        current_gen.summarized_es_value = summarized_es_value
        
        LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Preprocessing completed for aggregates '{aggregate_names}'. Command aliases: {current_gen.target_command_aliases}. Summary size: {len(str(summarized_es_value))} chars")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[GWT_SUBGRAPH] Preprocessing failed for aggregates '{aggregate_names}' in context '{bc_name}'", e)
        state.subgraphs.createGwtGeneratorByFunctionModel.is_failed = True
    
    return state

# 노드 정의: GWT 생성 실행
def generate_gwt_generation(state: State) -> State:
    """
    GWT 생성 실행
    - Generator를 통한 GWT 생성
    - 토큰 초과 확인 및 필요한 경우 요약 요청
    """
    current_gen = state.subgraphs.createGwtGeneratorByFunctionModel.current_generation
    if not current_gen:
        LogUtil.add_info_log(state, "[GWT_SUBGRAPH] No GWT generation task currently being processed, skipping generation")
        return state
        
    bc_name = current_gen.target_bounded_context.get("displayName", current_gen.target_bounded_context.get("name", "Unknown"))
    aggregate_names = ", ".join(current_gen.target_aggregate_names)
    retry_info = f" (retry {current_gen.retry_count})" if current_gen.retry_count > 0 else ""
    LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Generating GWT scenarios for aggregates '{aggregate_names}' in context '{bc_name}'{retry_info}")
    
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
            LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Applied summarized ES value for aggregates '{aggregate_names}' from summary generator")

        # 모델명 가져오기
        model_name = os.getenv("AI_MODEL") or f"{state.inputs.llmModel.model_vendor}:{state.inputs.llmModel.model_name}"
        
        # Generator 생성
        generator = CreateGWTGeneratorByFunction(
            model_name=model_name,
            client={
                "inputs": {
                    "summarizedESValue": current_gen.summarized_es_value,
                    "description": current_gen.description,
                    "targetCommandAliases": current_gen.target_command_aliases
                },
                "preferredLanguage": state.inputs.preferedLanguage
            }
        )
        
        # 토큰 초과 체크
        token_count = generator.get_token_count()
        model_max_input_limit = state.inputs.llmModel.model_max_input_limit
        
        LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Token usage for aggregates '{aggregate_names}': {token_count}/{model_max_input_limit}")
        
        if token_count > model_max_input_limit:  # 토큰 제한 초과 시 요약 처리
            LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Token limit exceeded for aggregates '{aggregate_names}' ({token_count} > {model_max_input_limit}), requesting ES value summary")
            
            # 빈 요약 ES 값을 사용하여 기본 요청 구조의 토큰 수 계산
            left_generator = CreateGWTGeneratorByFunction(
                model_name=model_name,
                client={
                    "inputs": {
                        "summarizedESValue": {},
                        "description": current_gen.description,
                        "targetCommandAliases": current_gen.target_command_aliases
                    },
                    "preferredLanguage": state.inputs.preferedLanguage
                }
            )

            left_token_count = model_max_input_limit - left_generator.get_token_count()
            if left_token_count < 50:
                # 너무 작은 토큰 수가 남은 경우 실패로 처리
                LogUtil.add_error_log(state, f"[GWT_SUBGRAPH] Insufficient token space for aggregates '{aggregate_names}' (remaining: {left_token_count})")
                state.subgraphs.createGwtGeneratorByFunctionModel.is_failed = True
                return state

            # ES 요약 생성 서브그래프 호출 준비
            # 요약 생성 모델 초기화
            state.subgraphs.esValueSummaryGeneratorModel = ESValueSummaryGeneratorModel(
                is_processing=False,
                is_complete=False,
                context=_build_request_context(current_gen),
                keys_to_filter=[],  # GWT 생성에 필요한 필터 설정
                max_tokens=left_token_count,
                token_calc_model_vendor=state.inputs.llmModel.model_vendor,
                token_calc_model_name=state.inputs.llmModel.model_name
            )
            
            # 토큰 초과시 요약 서브그래프 호출하고 현재 상태 반환
            current_gen.is_token_over_limit = True
            LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Prepared ES value summary request for aggregates '{aggregate_names}' (available tokens: {left_token_count})")
            return state
        
        # Generator 실행 결과
        LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Executing GWT generation for aggregates '{aggregate_names}' ({len(current_gen.target_command_aliases)} commands)")
        result = generator.generate(current_gen.retry_count > 0)
        
        # 결과에서 GWT 추출 및 적용
        commands_to_replace = []
        
        es_value = state.outputs.esValue.model_dump()
        if result and "result" in result:
            es_alias_trans_manager = EsAliasTransManager(es_value)
            scenario_count = len(result["result"])

            for scenario in result["result"]:
                target_command_id = es_alias_trans_manager.alias_to_uuid_dic.get(
                    scenario.get("targetCommandId"), scenario.get("targetCommandId")
                )
                
                if not target_command_id or target_command_id not in es_value["elements"]:
                    continue
                
                target_command = deepcopy(es_value["elements"][target_command_id])
                
                if not scenario.get("gwts") or len(scenario["gwts"]) == 0:
                    continue
                
                examples = _get_examples(scenario["gwts"], es_value)
                if not examples or len(examples) == 0:
                    continue
                
                target_command["examples"] = examples
                commands_to_replace.append(target_command)
        
        # 생성된 GWT 저장
        current_gen.commands_to_replace = commands_to_replace
        LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] GWT generation completed for aggregates '{aggregate_names}'. Generated {len(commands_to_replace)} GWT scenarios for {len(commands_to_replace)} commands")
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[GWT_SUBGRAPH] Failed to generate GWT for aggregates '{aggregate_names}' in context '{bc_name}'", e)
        if state.subgraphs.createGwtGeneratorByFunctionModel.current_generation:
            state.subgraphs.createGwtGeneratorByFunctionModel.current_generation.retry_count += 1

    return state

# 노드 정의: GWT 생성 후처리
def postprocess_gwt_generation(state: State) -> State:
    """
    GWT 생성 후처리 작업 수행
    - 생성된 GWT를 ES 모델에 적용
    """
    current_gen = state.subgraphs.createGwtGeneratorByFunctionModel.current_generation
    if not current_gen:
        LogUtil.add_info_log(state, "[GWT_SUBGRAPH] No GWT generation task currently being processed, skipping postprocessing")
        return state
        
    bc_name = current_gen.target_bounded_context.get("displayName", current_gen.target_bounded_context.get("name", "Unknown"))
    aggregate_names = ", ".join(current_gen.target_aggregate_names)
    LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Starting postprocessing for aggregates '{aggregate_names}' in context '{bc_name}'")
    
    try:

        # 생성된 GWT가 없으면 실패로 처리
        if not current_gen.commands_to_replace:
            LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] No GWTs generated for aggregates '{aggregate_names}', incrementing retry count")
            current_gen.retry_count += 1
            return state
        
        LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Applying {len(current_gen.commands_to_replace)} GWT scenarios to commands for aggregates '{aggregate_names}'")
        
        # ES 값의 복사본 생성
        es_value = deepcopy(state.outputs.esValue.model_dump())
        
        # 생성된 GWT를 ES 모델에 적용
        for command in current_gen.commands_to_replace:
            es_value["elements"][command["id"]] = command
        
        # ES 값 업데이트
        state.outputs.esValue.elements = es_value["elements"]
        current_gen.generation_complete = True
        
        LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Postprocessing completed successfully for aggregates '{aggregate_names}'. Updated {len(current_gen.commands_to_replace)} commands with GWT scenarios")
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[GWT_SUBGRAPH] Postprocessing failed for aggregates '{aggregate_names}' in context '{bc_name}'", e)
        if state.subgraphs.createGwtGeneratorByFunctionModel.current_generation:
            state.subgraphs.createGwtGeneratorByFunctionModel.current_generation.retry_count += 1
            state.subgraphs.createGwtGeneratorByFunctionModel.current_generation.commands_to_replace = []

    return state

# 노드 정의: GWT 생성 검증 및 완료 처리
def validate_gwt_generation(state: State) -> State:
    """
    GWT 생성 결과 검증 및 완료 처리
    - 생성 결과 검증
    - 완료 처리 또는 재시도 결정
    """
    current_gen = state.subgraphs.createGwtGeneratorByFunctionModel.current_generation
    if not current_gen:
        LogUtil.add_info_log(state, "[GWT_SUBGRAPH] No GWT generation task currently being processed, skipping validation")
        return state
        
    bc_name = current_gen.target_bounded_context.get("displayName", current_gen.target_bounded_context.get("name", "Unknown"))
    aggregate_names = ", ".join(current_gen.target_aggregate_names)
    LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] Validating GWT generation for aggregates '{aggregate_names}' in context '{bc_name}'")
    
    try:

        # 생성 완료 확인
        if current_gen.generation_complete and not state.subgraphs.createGwtGeneratorByFunctionModel.is_failed:
            # 변수 정리
            current_gen.target_bounded_context = {}
            current_gen.target_command_ids = []
            current_gen.target_aggregate_names = []
            current_gen.description = ""
            current_gen.summarized_es_value = {}
            current_gen.target_command_aliases = []
            current_gen.commands_to_replace = []

            # 완료된 작업을 완료 목록에 추가
            state.subgraphs.createGwtGeneratorByFunctionModel.completed_generations.append(current_gen)
            # 현재 작업 초기화
            state.subgraphs.createGwtGeneratorByFunctionModel.current_generation = None
            state.outputs.currentProgressCount = state.outputs.currentProgressCount + 1
            
            total_progress = state.outputs.totalProgressCount
            current_progress = state.outputs.currentProgressCount
            LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] GWT generation completed successfully for aggregates '{aggregate_names}'. Progress: {current_progress}/{total_progress}")

        elif current_gen.retry_count > state.subgraphs.createGwtGeneratorByFunctionModel.max_retry_count:
            # 최대 재시도 횟수 초과 시 실패로 처리하고 다음 작업으로 이동
            LogUtil.add_error_log(state, f"[GWT_SUBGRAPH] Maximum retry count exceeded for aggregates '{aggregate_names}' (retries: {current_gen.retry_count}). Moving to next task.")
            state.subgraphs.createGwtGeneratorByFunctionModel.is_failed = True
            state.subgraphs.createGwtGeneratorByFunctionModel.current_generation = None
        else:
            LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] GWT generation not yet complete for aggregates '{aggregate_names}', continuing process")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[GWT_SUBGRAPH] Validation failed for aggregates '{aggregate_names}' in context '{bc_name}'", e)
        state.subgraphs.createGwtGeneratorByFunctionModel.is_failed = True

    return state

# 단순 완료 처리를 위한 함수
def complete_processing(state: State) -> State:
    """
    GWT 생성 프로세스 완료
    """
    
    try:

        state.outputs.lastCompletedRootGraphNode = ResumeNodes["ROOT_GRAPH"]["CREATE_GWT"]
        state.outputs.lastCompletedSubGraphNode = ResumeNodes["CREATE_GWT"]["COMPLETE"]
        JobUtil.update_job_to_firebase_fire_and_forget(state)

        # 완료된 작업 수 정보 로그
        completed_count = len(state.subgraphs.createGwtGeneratorByFunctionModel.completed_generations)
        failed = state.subgraphs.createGwtGeneratorByFunctionModel.is_failed
        
        if failed:
            LogUtil.add_error_log(state, f"[GWT_SUBGRAPH] GWT generation process completed with failures. Successfully processed: {completed_count} aggregate tasks")
        else:
            LogUtil.add_info_log(state, f"[GWT_SUBGRAPH] GWT generation process completed successfully. Total processed: {completed_count} aggregate tasks")
        
        if not failed:
            # 변수 정리
            subgraph_model = state.subgraphs.createGwtGeneratorByFunctionModel
            subgraph_model.draft_options = {}
            subgraph_model.current_generation = None
            subgraph_model.completed_generations = []
            subgraph_model.pending_generations = []

    except Exception as e:
        LogUtil.add_exception_object_log(state, "[GWT_SUBGRAPH] Failed during GWT generation process completion", e)
        state.subgraphs.createGwtGeneratorByFunctionModel.is_failed = True

    return state

# 라우팅 함수: 다음 단계 결정
def decide_next_step(state: State) -> str:
    """
    다음 실행할 단계 결정
    """
    try :

        if state.subgraphs.createGwtGeneratorByFunctionModel.is_failed:
            return "complete"

        # 모든 작업이 완료되었으면 완료 상태로 이동
        if state.subgraphs.createGwtGeneratorByFunctionModel.all_complete:
            return "complete"
        
        # 현재 처리 중인 작업이 없으면 다음 작업 선택
        if not state.subgraphs.createGwtGeneratorByFunctionModel.current_generation:
            return "select_next"
        
        current_gen = state.subgraphs.createGwtGeneratorByFunctionModel.current_generation
        
        # 최대 재시도 횟수 초과 시 완료 상태로 이동
        if current_gen.retry_count > state.subgraphs.createGwtGeneratorByFunctionModel.max_retry_count:
            state.subgraphs.createGwtGeneratorByFunctionModel.is_failed = True
            return "complete"
        
        # 현재 작업이 완료되었으면 검증 단계로 이동
        if current_gen.generation_complete:
            return "validate"
        
        # 토큰 초과 시 요약 서브그래프 실행
        if current_gen.is_token_over_limit and hasattr(state.subgraphs.esValueSummaryGeneratorModel, 'is_complete'):
            if state.subgraphs.esValueSummaryGeneratorModel.is_complete:
                return "generate"
            else:
                return "es_value_summary_generator"
        
        # 전처리로 인한 요약 정보가 없을 경우, 전처리 단계로 이동
        if not current_gen.summarized_es_value:
            return "preprocess"
        
        # 기본적으로 생성 실행 단계로 이동
        if not current_gen.commands_to_replace:
            return "generate"
        
        # 생성된 GWT가 있으면 후처리 단계로 이동
        return "postprocess"
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[GWT_SUBGRAPH] Failed during decide_next_step", e)
        state.subgraphs.createGwtGeneratorByFunctionModel.is_failed = True
        return "complete"

# 요약 요청 컨텍스트 빌드 함수
def _build_request_context(current_gen: GWTGenerationState) -> str:
    """
    요약 요청 컨텍스트 빌드
    """
    target_bounded_context_name = current_gen.target_bounded_context.get("name", "")
    target_aggregate_names = current_gen.target_aggregate_names
    target_command_aliases = current_gen.target_command_aliases
    description = current_gen.description
    
    return f"""Focus on generating Given-When-Then (GWT) test scenarios for commands in the following context:

Bounded Context: {target_bounded_context_name}
Target Commands: {', '.join(target_command_aliases)}
Target Aggregates: {', '.join(target_aggregate_names)}

Business Requirements:
{description}

Please prioritize elements that are:
1. Directly related to the target commands and their associated events
2. Part of the same aggregate as the target commands
3. Referenced by the target commands or their events
4. Related to the business requirements provided
5. Part of the specified bounded context

This context is specifically for generating comprehensive GWT scenarios that validate the behavior and business rules of the target commands."""

# 서브그래프 생성 함수
def create_gwt_generator_by_function_subgraph() -> Callable:
    """
    Command GWT 생성 서브그래프 생성
    """
    # 서브그래프 정의
    subgraph = StateGraph(State)
    
    # 노드 추가
    subgraph.add_node("prepare", prepare_gwt_generation)
    subgraph.add_node("select_next", select_next_gwt_generation)
    subgraph.add_node("preprocess", preprocess_gwt_generation)
    subgraph.add_node("generate", generate_gwt_generation)
    subgraph.add_node("postprocess", postprocess_gwt_generation)
    subgraph.add_node("validate", validate_gwt_generation)
    subgraph.add_node("complete", complete_processing)
    subgraph.add_node("es_value_summary_generator", create_es_value_summary_generator_subgraph())
    
    # 엣지 추가 (라우팅)
    subgraph.add_conditional_edges(START, resume_from_create_gwt, {
        "prepare": "prepare",
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
        result = State(**compiled_subgraph.invoke(state))
        return result
    
    return run_subgraph


# 유틸리티 함수
def _get_examples(gwts: List[Dict[str, Any]], es_value: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    GWT 시나리오로부터 examples 데이터 구조를 생성하는 함수
    """
    examples = []
    for gwt in gwts:
        if not gwt.get("given") or not gwt.get("when") or not gwt.get("then"):
            continue
        
        given_element = _find_element_by_name(gwt["given"]["name"], es_value, "Aggregate")
        when_element = _find_element_by_name(gwt["when"]["name"], es_value, "Command")
        then_element = _find_element_by_name(gwt["then"]["name"], es_value, "Event")
        
        if not given_element or not when_element or not then_element:
            continue
            
        if not given_element.get("_type", "").endswith("Aggregate") or \
           not when_element.get("_type", "").endswith("Command") or \
           not then_element.get("_type", "").endswith("Event"):
            continue
        
        examples.append({
            "given": [{
                "type": "Aggregate",
                "name": gwt["given"]["name"],
                "value": _get_values_using_field_descriptors(gwt["given"]["values"], given_element.get("aggregateRoot", {}).get("fieldDescriptors", []))
            }],
            "when": [{
                "type": "Command",
                "name": gwt["when"]["name"],
                "value": _get_values_using_field_descriptors(gwt["when"]["values"], when_element.get("fieldDescriptors", []))
            }],
            "then": [{
                "type": "Event",
                "name": gwt["then"]["name"],
                "value": _get_values_using_field_descriptors(gwt["then"]["values"], then_element.get("fieldDescriptors", []))
            }]
        })
    
    return examples

def _find_element_by_name(name: str, es_value: Dict[str, Any], element_type: str) -> Dict[str, Any]:
    """
    이름으로 엘리먼트를 찾는 함수
    """
    for element in es_value.get("elements", {}).values():
        if element and element.get("name") == name and element_type in element.get("_type", ""):
            return element
    return {}

def _get_values_using_field_descriptors(values: Dict[str, Any], field_descriptors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    필드 설명자를 사용하여 값을 추출하는 함수
    """
    return_values = {}
    for field_descriptor in field_descriptors:
        field_name = field_descriptor.get("name")
        if field_name:
            return_values[field_name] = values.get(field_name, "N/A")
    return return_values