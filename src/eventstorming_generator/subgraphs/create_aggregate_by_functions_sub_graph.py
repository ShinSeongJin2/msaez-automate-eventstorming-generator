from typing import Dict, Any, List, Callable
from copy import deepcopy
from langgraph.graph import StateGraph, START
import os

from ..models import (
    AggregateGenerationState, State, ActionModel, EsValueModel, 
    ESValueSummaryGeneratorModel
)
from ..generators import (
    CreateAggregateActionsByFunction, AssignFieldsToActionsGenerator
)
from ..utils import EsActionsUtil, EsAliasTransManager, ESValueSummarizeWithFilter, JobUtil, LogUtil, CaseConvertUtil, EsUtils
from .es_value_summary_generator_sub_graph import create_es_value_summary_generator_subgraph
from ..constants import ResumeNodes


def resume_from_create_aggregates(state: State):
    try :

        if state.outputs.lastCompletedRootGraphNode == ResumeNodes["ROOT_GRAPH"]["CREATE_AGGREGATES"] and state.outputs.lastCompletedSubGraphNode:
            if state.outputs.lastCompletedSubGraphNode in ResumeNodes["CREATE_AGGREGATES"].values():
                LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Resuming from checkpoint: '{state.outputs.lastCompletedSubGraphNode}'")
                return state.outputs.lastCompletedSubGraphNode
            else:
                state.subgraphs.createAggregateByFunctionsModel.is_failed = True
                LogUtil.add_error_log(state, f"[AGGREGATE_SUBGRAPH] Invalid checkpoint node: '{state.outputs.lastCompletedSubGraphNode}'")
                return "complete"
        
        LogUtil.add_info_log(state, "[AGGREGATE_SUBGRAPH] Starting aggregate generation process")
        return "prepare"

    except Exception as e:
        LogUtil.add_exception_object_log(state, "[AGGREGATE_SUBGRAPH] Failed during resume_from_create_aggregates", e)
        state.subgraphs.createAggregateByFunctionsModel.is_failed = True
        return "complete"

# 노드 정의: 초안으로부터 Aggregate 생성 준비
def prepare_aggregate_generation(state: State) -> State:
    """
    초안으로부터 Aggregate 생성을 위한 준비 작업 수행
    - 초안 데이터 설정
    - DDL 필드 추출 및 애그리거트별 할당
    - 처리할 Aggregate 목록 초기화
    """
    
    try:

        LogUtil.add_info_log(state, "[AGGREGATE_SUBGRAPH] Starting aggregate generation preparation")

        # 이미 처리 중이면 상태 유지
        if state.subgraphs.createAggregateByFunctionsModel.is_processing:
            LogUtil.add_info_log(state, "[AGGREGATE_SUBGRAPH] Aggregate generation already in progress, maintaining state")
            return state
        
        # 초안 데이터 설정
        state.subgraphs.createAggregateByFunctionsModel.is_processing = True
        state.subgraphs.createAggregateByFunctionsModel.all_complete = False
        
        # 처리할 Aggregate 목록 초기화
        pending_generations = []
        
        # 각 Bounded Context별로 처리할 Aggregate 추출
        for bounded_context_name, bounded_context_data in state.inputs.selectedDraftOptions.items():
            target_bounded_context = {"name": bounded_context_name}
            if "boundedContext" in bounded_context_data:
                target_bounded_context.update(bounded_context_data["boundedContext"])
            
            structures = bounded_context_data.get("structure", [])
            LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Processing bounded context '{bounded_context_name}' with {len(structures)} aggregates")

            # 해당 Bounded Context의 구조 정보를 처리
            for index, structure in enumerate(structures):
                aggregate_name = structure.get("aggregate", {}).get("name", "Unknown")
                description = bounded_context_data.get("description", {})
                # 각 Aggregate 구조에 대한 생성 상태 초기화
                generation_state = AggregateGenerationState(
                    target_bounded_context=target_bounded_context,
                    target_aggregate=structure.get("aggregate", {}),
                    description=description,
                    original_description=description,
                    draft_option=[{
                        "aggregate": structure.get("aggregate", {}),
                        "enumerations": structure.get("enumerations", []),
                        "valueObjects": structure.get("valueObjects", [])
                    }],
                    is_accumulated=index > 0,  # 첫 번째가 아니면 누적 처리
                    retry_count=0,
                    generation_complete=False,
                    requirements=target_bounded_context.get("requirements", {}),
                    ddl_fields=[CaseConvertUtil.camel_case(field) for field in structure.get("previewAttributes", [])]  # 할당된 DDL 필드 설정
                )
                pending_generations.append(generation_state)
                LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Queued aggregate '{aggregate_name}' in context '{bounded_context_name}' with {len(structure.get('previewAttributes', []))} DDL fields (accumulated: {index > 0})")
        
        # 처리할 Aggregate 목록 저장
        state.subgraphs.createAggregateByFunctionsModel.pending_generations = pending_generations
        state.subgraphs.createAggregateByFunctionsModel.ddl_extraction_complete = True
        state.subgraphs.createAggregateByFunctionsModel.ddl_assignment_complete = True
        LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Preparation completed. Total aggregates to process: {len(pending_generations)}")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[AGGREGATE_SUBGRAPH] Failed during aggregate generation preparation", e)
        state.subgraphs.createAggregateByFunctionsModel.is_failed = True
    
    return state

# 노드 정의: 다음 생성할 Aggregate 선택
def select_next_aggregate(state: State) -> State:
    """
    다음에 생성할 Aggregate를 선택하고 현재 처리 상태로 설정
    """

    try:
        
        state.outputs.lastCompletedRootGraphNode = ResumeNodes["ROOT_GRAPH"]["CREATE_AGGREGATES"]
        state.outputs.lastCompletedSubGraphNode = ResumeNodes["CREATE_AGGREGATES"]["SELECT_NEXT"]
        JobUtil.update_job_to_firebase_fire_and_forget(state)

        pending_count = len(state.subgraphs.createAggregateByFunctionsModel.pending_generations)
        completed_count = len(state.subgraphs.createAggregateByFunctionsModel.completed_generations)
        
        LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Selecting next aggregate. Pending: {pending_count}, Completed: {completed_count}")

        # 모든 처리가 완료되었는지 확인
        if (not state.subgraphs.createAggregateByFunctionsModel.pending_generations and 
            not state.subgraphs.createAggregateByFunctionsModel.current_generation):
            state.subgraphs.createAggregateByFunctionsModel.all_complete = True
            state.subgraphs.createAggregateByFunctionsModel.is_processing = False
            LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] All aggregate generations completed successfully. Total processed: {completed_count}")
            return state
        
        # 현재 처리 중인 작업이 있으면 상태 유지
        if state.subgraphs.createAggregateByFunctionsModel.current_generation:
            current = state.subgraphs.createAggregateByFunctionsModel.current_generation
            aggregate_name = current.target_aggregate.get("name", "Unknown")
            bc_name = current.target_bounded_context.get("name", "Unknown")
            LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Current generation in progress: '{aggregate_name}' in context '{bc_name}'")
            return state
        
        # 대기 중인 Aggregate가 있으면 첫 번째 항목을 현재 처리 상태로 설정
        if state.subgraphs.createAggregateByFunctionsModel.pending_generations:
            current_gen = state.subgraphs.createAggregateByFunctionsModel.pending_generations.pop(0)
            state.subgraphs.createAggregateByFunctionsModel.current_generation = current_gen
            
            aggregate_name = current_gen.target_aggregate.get("name", "Unknown")
            bc_name = current_gen.target_bounded_context.get("name", "Unknown")
            LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Selected next aggregate: '{aggregate_name}' in context '{bc_name}' (remaining: {len(state.subgraphs.createAggregateByFunctionsModel.pending_generations)})")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[AGGREGATE_SUBGRAPH] Failed to select next aggregate", e)
        state.subgraphs.createAggregateByFunctionsModel.is_failed = True
    
    return state

# 노드 정의: Aggregate 생성 전처리
def preprocess_aggregate_generation(state: State) -> State:
    """
    Aggregate 생성을 위한 전처리 작업 수행
    - 요약된 ES 값 생성
    - ID 변환 처리
    - 기존 요소 제거 등
    """
    current_gen = state.subgraphs.createAggregateByFunctionsModel.current_generation
    if not current_gen:
        LogUtil.add_info_log(state, "[AGGREGATE_SUBGRAPH] No current generation found, skipping preprocessing")
        return state
        
    aggregate_name = current_gen.target_aggregate.get("name", "Unknown")
    bc_name = current_gen.target_bounded_context.get("name", "Unknown")
    LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Starting preprocessing for aggregate '{aggregate_name}' in context '{bc_name}'")
    
    try:
        # 기능 요구사항에 라인 번호 추가
        if current_gen.description:
            current_gen.description = EsUtils.add_line_numbers_to_description(current_gen.description)

        # 별칭 변환 관리자 생성
        es_alias_trans_manager = EsAliasTransManager(state.outputs.esValue.model_dump())
        
        # 첫 번째 Aggregate 생성인 경우 이전 Bounded Context 관련 요소 제거
        target_bc_removed_es_value = deepcopy(state.outputs.esValue.model_dump())
        if not current_gen.is_accumulated:
            LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Removing previous elements for fresh start in context '{bc_name}'")
            _remove_prev_bounded_context_related_elements(
                current_gen.target_bounded_context.get("name", ""), 
                target_bc_removed_es_value
            )
        
        # 요약된 ES 값 생성
        summarized_es_value = ESValueSummarizeWithFilter.get_summarized_es_value(
            target_bc_removed_es_value,
            ESValueSummarizeWithFilter.KEY_FILTER_TEMPLATES["aggregateOuterStickers"],
            es_alias_trans_manager
        )
        
        # 요약된 ES 값 저장
        current_gen.summarized_es_value = summarized_es_value
        
        # 클래스 ID 속성 제거 (필요한 경우)
        current_gen.draft_option = _remove_class_id_properties(deepcopy(current_gen.draft_option))  
        LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Preprocessing completed for aggregate '{aggregate_name}'. Summary size: {len(str(summarized_es_value))} chars")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[AGGREGATE_SUBGRAPH] Preprocessing failed for aggregate '{aggregate_name}'", e)
        state.subgraphs.createAggregateByFunctionsModel.is_failed = True
    
    return state

# 노드 정의: DDL 필드 검증 및 설정
def extract_ddl_fields(state: State) -> State:
    """
    사전에 할당된 DDL 필드를 extracted_ddl_fields로 설정
    (실제 추출은 prepare_aggregate_generation에서 이미 완료됨)
    """
    current_gen = state.subgraphs.createAggregateByFunctionsModel.current_generation
    if not current_gen:
        LogUtil.add_info_log(state, "[AGGREGATE_SUBGRAPH] No current generation found, skipping DDL field setup")
        return state

    aggregate_name = current_gen.target_aggregate.get("name", "Unknown")
    bc_name = current_gen.target_bounded_context.get("name", "Unknown")
    LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Setting up DDL fields for aggregate '{aggregate_name}' in context '{bc_name}'")
    current_gen.ddl_extraction_attempted = True

    try:
        # 사전에 할당된 DDL 필드를 extracted_ddl_fields로 설정
        if current_gen.ddl_fields:
            current_gen.extracted_ddl_fields = current_gen.ddl_fields.copy()
            LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Set {len(current_gen.extracted_ddl_fields)} DDL fields for aggregate '{aggregate_name}'")
        else:
            LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] No DDL fields assigned to aggregate '{aggregate_name}'")
            current_gen.extracted_ddl_fields = []

    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[AGGREGATE_SUBGRAPH] Failed during DDL field setup for aggregate '{aggregate_name}'", e)
        # Do not fail the entire process, just log and continue
    
    return state

# 노드 정의: Aggregate 생성 실행
def generate_aggregate(state: State) -> State:
    """
    Aggregate 생성 실행
    - Generator를 통한 Aggregate 액션 생성
    """
    current_gen = state.subgraphs.createAggregateByFunctionsModel.current_generation
    if not current_gen:
        LogUtil.add_info_log(state, "[AGGREGATE_SUBGRAPH] No current generation found, skipping generation")
        return state
        
    aggregate_name = current_gen.target_aggregate.get("name", "Unknown")
    bc_name = current_gen.target_bounded_context.get("name", "Unknown")
    retry_info = f" (retry {current_gen.retry_count})" if current_gen.retry_count > 0 else ""
    LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Generating aggregate '{aggregate_name}' in context '{bc_name}'{retry_info}")
    
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
            LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Applied summarized ES value for '{aggregate_name}' from summary generator")

        # 모델명 가져오기
        model_name = os.getenv("AI_MODEL") or f"{state.inputs.llmModel.model_vendor}:{state.inputs.llmModel.model_name}"

        # Generator 생성
        generator = CreateAggregateActionsByFunction(
            model_name=model_name,
            client={
                "inputs": {
                    "summarizedESValue": current_gen.summarized_es_value,
                    "targetBoundedContext": current_gen.target_bounded_context,
                    "description": current_gen.description,
                    "draftOption": current_gen.draft_option,
                    "targetAggregate": current_gen.target_aggregate,
                    "extractedDdlFields": current_gen.extracted_ddl_fields
                },
                "preferredLanguage": state.inputs.preferedLanguage
            }
        )
        
        # 토큰 초과 체크
        token_count = generator.get_token_count()
        model_max_input_limit = state.inputs.llmModel.model_max_input_limit
        
        if token_count > model_max_input_limit:
            LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Token limit exceeded for '{aggregate_name}' ({token_count} > {model_max_input_limit}), requesting ES value summary")
            
            left_generator = CreateAggregateActionsByFunction(
                model_name=model_name,
                client={
                    "inputs": {
                        "summarizedESValue": {},
                        "targetBoundedContext": current_gen.target_bounded_context,
                        "description": current_gen.description,
                        "draftOption": current_gen.draft_option,
                        "targetAggregate": current_gen.target_aggregate,
                        "extractedDdlFields": current_gen.extracted_ddl_fields
                    },
                    "preferredLanguage": state.inputs.preferedLanguage
                }
            )

            left_token_count = model_max_input_limit - left_generator.get_token_count()
            if left_token_count < 50:
                LogUtil.add_error_log(state, f"[AGGREGATE_SUBGRAPH] Insufficient token space for '{aggregate_name}' even after removing ES value")
                state.subgraphs.createAggregateByFunctionsModel.is_failed = True
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
            LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Prepared ES value summary request for '{aggregate_name}' (available tokens: {left_token_count})")
            return state
        
        # Generator 실행 결과
        LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Executing generation for '{aggregate_name}' with {token_count} tokens")
        result = generator.generate(current_gen.retry_count > 0)
        
        # 결과에서 액션 추출
        actions = []
        if result and "result" in result:
            aggregate_actions = result["result"].get("aggregateActions", [])
            value_object_actions = result["result"].get("valueObjectActions", [])
            enumeration_actions = result["result"].get("enumerationActions", [])
            
            actions = aggregate_actions + value_object_actions + enumeration_actions
        
        actionModels = [ActionModel(**action) for action in actions]
        for action in actionModels:
            action.type = "create"
        
        # 생성된 액션 저장
        current_gen.created_actions = actionModels
        LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Generated {len(actionModels)} actions for aggregate '{aggregate_name}' (aggregates: {len(result.get('result', {}).get('aggregateActions', []))}, VOs: {len(result.get('result', {}).get('valueObjectActions', []))}, enums: {len(result.get('result', {}).get('enumerationActions', []))})")
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[AGGREGATE_SUBGRAPH] Failed to generate aggregate '{aggregate_name}'", e)
        if state.subgraphs.createAggregateByFunctionsModel.current_generation:
            state.subgraphs.createAggregateByFunctionsModel.current_generation.retry_count += 1
    
    return state

# 노드 정의: Aggregate 생성 후처리
def postprocess_aggregate_generation(state: State) -> State:
    """
    Aggregate 생성 후처리 작업 수행
    - 생성된 액션 검증
    - ID 변환
    - ES 값 업데이트
    """
    current_gen = state.subgraphs.createAggregateByFunctionsModel.current_generation
    if not current_gen:
        LogUtil.add_info_log(state, "[AGGREGATE_SUBGRAPH] No current generation found, skipping postprocessing")
        return state
        
    aggregate_name = current_gen.target_aggregate.get("name", "Unknown")
    bc_name = current_gen.target_bounded_context.get("name", "Unknown")
    LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Starting postprocessing for aggregate '{aggregate_name}' in context '{bc_name}'")
    
    try:
        # 생성된 액션이 없으면 실패로 처리
        if not current_gen.created_actions:
            LogUtil.add_error_log(state, f"[AGGREGATE_SUBGRAPH] No actions generated for aggregate '{aggregate_name}', incrementing retry count")
            current_gen.retry_count += 1
            return state
        
        LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Processing {len(current_gen.created_actions)} actions for aggregate '{aggregate_name}'")
        
        # ES 값의 복사본 생성
        es_value = EsValueModel(**deepcopy(state.outputs.esValue.model_dump()))
        es_alias_trans_manager = EsAliasTransManager(es_value)
        
        actions = _filter_valid_property_actions(current_gen.created_actions)
        if not current_gen.is_action_postprocess_completed:
            # 액션 필터링 및 ID 변환
            actions = es_alias_trans_manager.trans_to_uuid_in_actions(actions)
            
            # Bounded Context ID 복원
            _restore_actions(
                actions, 
                es_value, 
                current_gen.target_bounded_context.get("name", "")
            )
            
            # Aggregate ID 필터링
            actions = _filter_valid_aggregate_id_actions(
                actions,
                current_gen.target_aggregate.get("name", "")
            )
            
            LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Filtered to {len(actions)} valid actions for aggregate '{aggregate_name}'")

        # DDL 필드 포함 여부 검증
        missing_fields = []
        if current_gen.extracted_ddl_fields:
            all_generated_fields = set()
            for action in actions:
                if action.get("args") and "properties" in action.get("args", {}):
                    for prop in action.get("args", {}).get("properties", []):
                        if prop.get("name"):
                            all_generated_fields.add(CaseConvertUtil.camel_case(prop.get("name")))
            
            extracted_fields_set = {f for f in current_gen.extracted_ddl_fields}
            missing_fields = list(extracted_fields_set - all_generated_fields)
            
            if missing_fields:
                current_gen.missing_ddl_fields = missing_fields
                current_gen.created_actions = [ActionModel(**action) for action in actions] # 필터링된 액션 저장
                current_gen.is_action_postprocess_completed = True
                LogUtil.add_warning_log(state, f"[AGGREGATE_SUBGRAPH] DDL fields missing for '{aggregate_name}': {missing_fields}. Routing to fix.")
                return state # 다음 단계(assign_missing_fields)로 보냄
            else:
                LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] All {len(extracted_fields_set)} DDL fields successfully included for '{aggregate_name}'.")

        # ES 값 업데이트를 위한 준비
        es_value_to_modify = EsValueModel(**deepcopy(es_value.model_dump()))
        
        # 이전 Bounded Context 관련 요소 제거 (필요한 경우)
        if not current_gen.is_accumulated:
            LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Removing previous elements for '{aggregate_name}' as this is not accumulated")
            _remove_prev_bounded_context_related_elements(
                current_gen.target_bounded_context.get("name", ""),
                es_value_to_modify
            )
        
        # SourceReferences 후처리
        try:
            EsUtils.convert_source_references(actions, current_gen.original_description, state, "[AGGREGATE_SUBGRAPH]")
            LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Successfully converted source references for '{aggregate_name}'")
        except Exception as e:
            LogUtil.add_exception_object_log(state, f"[AGGREGATE_SUBGRAPH] Failed to convert source references for '{aggregate_name}'", e)
            # 후처리 실패시에도 계속 진행하되, 에러 로그를 남김

        updated_es_value = EsActionsUtil.apply_actions(
            es_value_to_modify,
            actions,
            state.inputs.userInfo,
            state.inputs.information
        )
        
        # ES 값 업데이트
        state.outputs.esValue = updated_es_value
        current_gen.generation_complete = True
        
        LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Postprocessing completed successfully for aggregate '{aggregate_name}'. Applied {len(actions)} actions to ES value")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[AGGREGATE_SUBGRAPH] Postprocessing failed for aggregate '{aggregate_name}'", e)
        if state.subgraphs.createAggregateByFunctionsModel.current_generation:
            current_gen = state.subgraphs.createAggregateByFunctionsModel.current_generation
            current_gen.retry_count += 1
            current_gen.created_actions = []
    
    return state

# 노드 정의: 누락된 DDL 필드 할당
def assign_missing_fields(state: State) -> State:
    """
    누락된 DDL 필드를 기존 Aggregate 또는 ValueObject에 할당
    """
    current_gen = state.subgraphs.createAggregateByFunctionsModel.current_generation
    if not current_gen or not current_gen.missing_ddl_fields:
        LogUtil.add_info_log(state, "[AGGREGATE_SUBGRAPH] No missing fields to assign, skipping.")
        return state

    aggregate_name = current_gen.target_aggregate.get("name", "Unknown")
    LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Starting assignment for {len(current_gen.missing_ddl_fields)} missing fields for aggregate '{aggregate_name}'")

    try:
        model_name = os.getenv("AI_MODEL") or f"{state.inputs.llmModel.model_vendor}:{state.inputs.llmModel.model_name}"
        

        elementAliasToUUIDDic = {}
        existing_actions = []
        for action in current_gen.created_actions:
            if action.objectType == "Aggregate":
                aggregate_alias = "agg-" + action.args["aggregateName"]
                elementAliasToUUIDDic[aggregate_alias] = action.ids["aggregateId"]

                dumped_action = action.model_dump()
                dumped_action["ids"]["aggregateId"] = aggregate_alias
                if "boundedContextId" in dumped_action["ids"]:
                    del dumped_action["ids"]["boundedContextId"]
                if "sourceReferences" in dumped_action["args"]:
                    del dumped_action["args"]["sourceReferences"]
                if "properties" in dumped_action["args"]:
                    for prop in dumped_action["args"]["properties"]:
                        if "sourceReferences" in prop:
                            del prop["sourceReferences"]
                existing_actions.append(dumped_action)

            elif action.objectType == "ValueObject":
                value_object_alias = "vo-" + action.args["valueObjectName"]
                elementAliasToUUIDDic[value_object_alias] = action.ids["valueObjectId"]

                dumped_action = action.model_dump()
                dumped_action["ids"]["valueObjectId"] = value_object_alias
                if "boundedContextId" in dumped_action["ids"]:
                    del dumped_action["ids"]["boundedContextId"]
                if "sourceReferences" in dumped_action["args"]:
                    del dumped_action["args"]["sourceReferences"]
                if "properties" in dumped_action["args"]:
                    for prop in dumped_action["args"]["properties"]:
                        if "sourceReferences" in prop:
                            del prop["sourceReferences"]
                existing_actions.append(dumped_action)


        generator_inputs = {
            "description": current_gen.description,
            "existingActions": existing_actions,
            "missingFields": current_gen.missing_ddl_fields
        }

        generator = AssignFieldsToActionsGenerator(
            model_name=model_name,
            client={"inputs": generator_inputs, "preferredLanguage": state.inputs.preferedLanguage}
        )
        
        result = generator.generate()


        if not result or "result" not in result or "assignments" not in result["result"]:
            LogUtil.add_error_log(state, f"[AGGREGATE_SUBGRAPH] AssignFieldsToActionsGenerator failed for '{aggregate_name}'. Retrying.")
            current_gen.retry_count += 1
            return state

        assignments = result["result"]["assignments"]
        LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Generator proposed assignments for {len(assignments)} parents.")

        actions_map = {action.ids["aggregateId"] if action.objectType == "Aggregate" else action.ids["valueObjectId"]: action for action in current_gen.created_actions if action.objectType in ["Aggregate", "ValueObject"]}

        for assignment in assignments:
            parent_id = elementAliasToUUIDDic[assignment.get("parent_id")]
            if parent_id in actions_map:
                parent_action = actions_map[parent_id]
                props_to_add = assignment.get("properties_to_add", [])
                for prop_data in props_to_add:
                    parent_action.args["properties"].append(prop_data)
            else:
                LogUtil.add_warning_log(state, f"[AGGREGATE_SUBGRAPH] Could not find parent with ID '{parent_id}' to assign fields.")

        current_gen.missing_ddl_fields = []
        current_gen.retry_count = 0 # Reset retry count after successful assignment to allow postprocessing to try again

    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[AGGREGATE_SUBGRAPH] Failed during field assignment for '{aggregate_name}'", e)
        current_gen.retry_count += 1
    
    return state

# 노드 정의: Aggregate 생성 검증 및 완료 처리
def validate_aggregate_generation(state: State) -> State:
    """
    Aggregate 생성 결과 검증 및 완료 처리
    - 생성 결과 검증
    - 완료 처리 또는 재시도 결정
    """
    current_gen = state.subgraphs.createAggregateByFunctionsModel.current_generation
    if not current_gen:
        LogUtil.add_info_log(state, "[AGGREGATE_SUBGRAPH] No current generation found, skipping validation")
        return state
        
    aggregate_name = current_gen.target_aggregate.get("name", "Unknown")
    bc_name = current_gen.target_bounded_context.get("name", "Unknown")
    LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Validating generation for aggregate '{aggregate_name}' in context '{bc_name}'")
    
    try:
        # 생성 완료 확인
        if current_gen.generation_complete and not state.subgraphs.createAggregateByFunctionsModel.is_failed:
            # 변수 정리
            current_gen.target_bounded_context = {}
            current_gen.target_aggregate = {}
            current_gen.description = ""
            current_gen.original_description = ""
            current_gen.draft_option = []
            current_gen.summarized_es_value = {}
            current_gen.created_actions = []

            # 완료된 작업을 완료 목록에 추가
            state.subgraphs.createAggregateByFunctionsModel.completed_generations.append(current_gen)
            # 현재 작업 초기화
            state.subgraphs.createAggregateByFunctionsModel.current_generation = None
            state.outputs.currentProgressCount = state.outputs.currentProgressCount + 1
            
            total_progress = state.outputs.totalProgressCount
            current_progress = state.outputs.currentProgressCount
            LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Aggregate '{aggregate_name}' generation completed successfully. Progress: {current_progress}/{total_progress}")
        else:
            LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Aggregate '{aggregate_name}' generation not yet complete, continuing process")

    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[AGGREGATE_SUBGRAPH] Validation failed for aggregate '{aggregate_name}'", e)
        state.subgraphs.createAggregateByFunctionsModel.is_failed = True

    return state

# 단순 완료 처리를 위한 함수
def complete_processing(state: State) -> State:
    """
    Aggregate 생성 프로세스 완료
    """
    
    try:

        state.outputs.lastCompletedRootGraphNode = ResumeNodes["ROOT_GRAPH"]["CREATE_AGGREGATES"]
        state.outputs.lastCompletedSubGraphNode = ResumeNodes["CREATE_AGGREGATES"]["COMPLETE"]
        JobUtil.update_job_to_firebase_fire_and_forget(state)

        completed_count = len(state.subgraphs.createAggregateByFunctionsModel.completed_generations)
        failed = state.subgraphs.createAggregateByFunctionsModel.is_failed
        
        if failed:
            LogUtil.add_error_log(state, f"[AGGREGATE_SUBGRAPH] Aggregate generation process completed with failures. Successfully processed: {completed_count} aggregates")
        else:
            LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Aggregate generation process completed successfully. Total processed: {completed_count} aggregates")

        if not failed:
            # 변수 정리
            subgraph_model = state.subgraphs.createAggregateByFunctionsModel
            subgraph_model.current_generation = None
            subgraph_model.completed_generations = []
            subgraph_model.pending_generations = []
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[AGGREGATE_SUBGRAPH] Failed during process completion", e)
        state.subgraphs.createAggregateByFunctionsModel.is_failed = True
    
    return state

# 라우팅 함수: 다음 단계 결정
def decide_next_step(state: State) -> str:
    """
    다음 실행할 단계 결정
    """
    try :

        # 작업 실패시에 강제로 완료 상태로 이동
        if state.subgraphs.createAggregateByFunctionsModel.is_failed:
            return "complete"

        # 모든 작업이 완료되었으면 완료 상태로 이동
        if state.subgraphs.createAggregateByFunctionsModel.all_complete:
            return "complete"
        
        # 현재 처리 중인 작업이 없으면 다음 작업 선택
        if not state.subgraphs.createAggregateByFunctionsModel.current_generation:
            return "select_next"
        
        current_gen = state.subgraphs.createAggregateByFunctionsModel.current_generation
        if current_gen.retry_count > state.subgraphs.createAggregateByFunctionsModel.max_retry_count:
            state.subgraphs.createAggregateByFunctionsModel.is_failed = True
            return "complete"

        # 현재 작업이 완료되었으면 검증 단계로 이동
        if current_gen.generation_complete:
            return "validate"
        
        if current_gen.is_token_over_limit and hasattr(state.subgraphs.esValueSummaryGeneratorModel, 'is_complete'):
            if state.subgraphs.esValueSummaryGeneratorModel.is_complete:
                return "generate"
            else:
                return "es_value_summary_generator"
        
        # 전치리로 인한 요약 정보가 없을 경우, 전처리 단계로 이동
        if not current_gen.summarized_es_value:
            return "preprocess"
        
        # DDL 필드 설정 단계
        if current_gen.ddl_fields and not current_gen.ddl_extraction_attempted:
            return "extract_ddl_fields"
        
        # 누락된 필드가 있으면 할당 단계로 이동
        if current_gen.missing_ddl_fields:
            return "assign_missing_fields"
        
        # 기본적으로 생성 실행 단계로 이동
        if not current_gen.created_actions:
            return "generate"
        
        # 생성된 액션이 있으면 후처리 단계로 이동
        return "postprocess"

    except Exception as e:
        LogUtil.add_exception_object_log(state, "[AGGREGATE_SUBGRAPH] Failed during decide_next_step", e)
        state.subgraphs.createAggregateByFunctionsModel.is_failed = True
        return "complete"

# 서브그래프 생성 함수
def create_aggregate_by_functions_subgraph() -> Callable:
    """
    Aggregate 생성 서브그래프 생성
    """
    # 서브그래프 정의
    subgraph = StateGraph(State)
    
    # 노드 추가
    subgraph.add_node("prepare", prepare_aggregate_generation)
    subgraph.add_node("select_next", select_next_aggregate)
    subgraph.add_node("preprocess", preprocess_aggregate_generation)
    subgraph.add_node("extract_ddl_fields", extract_ddl_fields)
    subgraph.add_node("generate", generate_aggregate)
    subgraph.add_node("postprocess", postprocess_aggregate_generation)
    subgraph.add_node("assign_missing_fields", assign_missing_fields)
    subgraph.add_node("validate", validate_aggregate_generation)
    subgraph.add_node("complete", complete_processing)
    subgraph.add_node("es_value_summary_generator", create_es_value_summary_generator_subgraph())
    
    # 엣지 추가 (라우팅)
    subgraph.add_conditional_edges(START, resume_from_create_aggregates, {
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
            "extract_ddl_fields": "extract_ddl_fields",
            "complete": "complete"
        }
    )

    subgraph.add_conditional_edges(
        "extract_ddl_fields",
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
            "assign_missing_fields": "assign_missing_fields",
            "complete": "complete"
        }
    )

    subgraph.add_conditional_edges(
        "assign_missing_fields",
        decide_next_step,
        {
            "assign_missing_fields": "assign_missing_fields",
            "postprocess": "postprocess",
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


# 유틸리티 함수
def _remove_class_id_properties(draft_option: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    클래스 ID 속성 제거
    """
    if not isinstance(draft_option, list):
        return draft_option
    
    return [
        {
            **option,
            "valueObjects": [
                vo for vo in option.get("valueObjects", [])
                if not vo.get("referencedAggregate")
            ] if "valueObjects" in option else []
        }
        for option in draft_option
    ]

def _filter_valid_property_actions(actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    유효한 속성 액션 필터링
    """
    # 기본 검증
    actions = [
        action for action in actions
        if action.get("actionName") and action.get("objectType") and 
           action.get("ids") and action.get("ids", {}).get("aggregateId")
    ]
    
    # 객체 타입별 검증
    actions = [
        action for action in actions
        if (action.get("objectType") == "Aggregate") or
           (action.get("objectType") == "ValueObject" and 
            action.get("ids", {}).get("valueObjectId")) or
           (action.get("objectType") == "Enumeration" and 
            action.get("ids", {}).get("enumerationId"))
    ]
    
    # 속성 검증
    for action in actions:
        if action.get("args") and "properties" in action["args"]:
            action["args"]["properties"] = [
                prop for prop in action["args"]["properties"]
                if prop.get("name")
            ]
    
    return actions

def _filter_valid_aggregate_id_actions(actions: List[Dict[str, Any]], target_aggregate_name: str) -> List[Dict[str, Any]]:
    """
    유효한 Aggregate ID 액션 필터링
    """
    target_aggregate_name = target_aggregate_name.lower()
    
    # 유효한 Aggregate ID 목록 추출
    valid_aggregate_ids = [
        action.get("ids", {}).get("aggregateId")
        for action in actions
        if (action.get("objectType") == "Aggregate" and
            action.get("args") and
            action.get("args").get("aggregateName") and
            action.get("args").get("aggregateName").lower() == target_aggregate_name)
    ]
    
    # 유효한 Aggregate ID를 가진 액션만 필터링
    return [
        action for action in actions
        if action.get("ids", {}).get("aggregateId") in valid_aggregate_ids
    ]

def _restore_actions(actions: List[Dict[str, Any]], es_value: Dict[str, Any], target_bounded_context_name: str) -> None:
    """
    액션 데이터 복원
    """
    # 대상 Bounded Context 찾기
    target_bounded_context = _get_target_bounded_context(es_value, target_bounded_context_name)
    
    # Bounded Context ID 복원
    for action in actions:
        if action.get("objectType") in ["Aggregate", "Entity", "ValueObject", "Enumeration"]:
            action["ids"] = {
                "boundedContextId": target_bounded_context.get("id"),
                **action.get("ids", {})
            }

def _get_target_bounded_context(es_value: Dict[str, Any], target_bounded_context_name: str) -> Dict[str, Any]:
    """
    대상 Bounded Context 찾기
    """
    for element in es_value.get("elements", {}).values():
        if (element and 
            element.get("_type") == "org.uengine.modeling.model.BoundedContext" and
            element.get("name", "").lower() == target_bounded_context_name.lower()):
            return element
    
    # 찾지 못한 경우 빈 객체 반환
    return {}

def _remove_prev_bounded_context_related_elements(target_bounded_context_name: str, es_value: Dict[str, Any]) -> None:
    """
    이전 Bounded Context 관련 요소 제거
    """
    # 대상 Bounded Context 찾기
    target_bounded_context = _get_target_bounded_context(es_value, target_bounded_context_name)
    if not target_bounded_context:
        return

    # Bounded Context 관련 요소만 포함된 ES 값 얻기
    es_value_to_remove = _get_only_bounded_context_related_summarized_es_value(
        es_value, target_bounded_context_name
    )
    
    # 관련 요소 제거 (Bounded Context 자체는 유지)
    for element_id, element in es_value_to_remove.get("elements", {}).items():
        if element and element.get("id") != target_bounded_context.get("id"):
            es_value["elements"][element_id] = None
    
    # 관련 관계 제거
    for relation_id in es_value_to_remove.get("relations", {}).keys():
        es_value["relations"][relation_id] = None

def _get_only_bounded_context_related_summarized_es_value(es_value: Dict[str, Any], target_bounded_context_name: str) -> Dict[str, Any]:
    """
    Bounded Context 관련 요소만 포함된 요약된 ES 값 얻기
    """
    # 대상 Bounded Context 찾기
    target_bounded_context = _get_target_bounded_context(es_value, target_bounded_context_name)
    if not target_bounded_context:
        return {"elements": {}, "relations": {}}
    
    # Bounded Context 관련 여부 확인 함수
    def is_have_target_bounded_context(element):
        return ((isinstance(element.get("boundedContext"), str) and 
                 element["boundedContext"] == target_bounded_context.get("id")) or
                (isinstance(element.get("boundedContext"), dict) and 
                 element["boundedContext"].get("id") == target_bounded_context.get("id")))
    
    # 관련 요소 추출
    bc_related_es_value = {"elements": {}, "relations": {}}
    bc_related_es_value["elements"][target_bounded_context.get("id")] = target_bounded_context
    
    for element_id, element in es_value.get("elements", {}).items():
        if element and is_have_target_bounded_context(element):
            bc_related_es_value["elements"][element_id] = element
    
    # 관련 관계 추출
    for relation_id, relation in es_value.get("relations", {}).items():
        if relation and relation.get("sourceElement") and relation.get("targetElement"):
            if (is_have_target_bounded_context(relation["sourceElement"]) or 
                is_have_target_bounded_context(relation["targetElement"])):
                bc_related_es_value["relations"][relation_id] = relation
    
    return bc_related_es_value

# 요약 요청 컨텍스트 빌드 함수
def _build_request_context(current_gen) -> str:
    """
    요약 요청 컨텍스트 빌드
    """
    target_aggregate = current_gen.target_aggregate
    aggregate_name = target_aggregate.get("name", "")
    aggregate_alias = target_aggregate.get("alias", "")
    bounded_context_name = current_gen.target_bounded_context.get("name", "")
    description = current_gen.description
    
    aggregate_structure = current_gen.draft_option[0] if current_gen.draft_option else {}
    
    has_value_objects = (
        "valueObjects" in aggregate_structure and 
        isinstance(aggregate_structure["valueObjects"], list) and 
        len(aggregate_structure["valueObjects"]) > 0
    )
    
    has_enumerations = (
        "enumerations" in aggregate_structure and 
        isinstance(aggregate_structure["enumerations"], list) and 
        len(aggregate_structure["enumerations"]) > 0
    )
    
    return f"""Task: Creating {aggregate_name} Aggregate in {bounded_context_name} Bounded Context
    
Business Context:
{description}

Aggregate Structure:
- Creating new aggregate '{aggregate_name}'{ f" ({aggregate_alias})" if aggregate_alias else "" }
- Will contain {("value objects" if has_value_objects else "")}{"and " if has_value_objects and has_enumerations else ""}{"enumerations" if has_enumerations else ""}
- Part of {bounded_context_name} domain

Focus:
- Elements directly related to {aggregate_name} aggregate
- Supporting elements within {bounded_context_name} bounded context
- Essential domain relationships and dependencies"""