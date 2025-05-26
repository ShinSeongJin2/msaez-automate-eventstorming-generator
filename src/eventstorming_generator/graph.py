from langgraph.graph import StateGraph, START, END
from typing import Dict, Any

from eventstorming_generator.models import ActionModel, State
from eventstorming_generator.utils import EsActionsUtil, JobUtil, LogUtil
from eventstorming_generator.subgraphs import create_aggregate_by_functions_subgraph, create_aggregate_class_id_by_drafts_subgraph, create_command_actions_by_function_subgraph, create_policy_actions_by_function_subgraph, create_gwt_generator_by_function_subgraph

def validate_input(state: State):
    if not state.inputs.jobId or not JobUtil.is_valid_job_id(state.inputs.jobId):
        LogUtil.add_error_log(state, f"Invalid jobId: {state.inputs.jobId}")
        return "complete"

    return state

def create_bounded_contexts(state: State):
    LogUtil.add_info_log(state, "Creating bounded contexts...")
    state.outputs.totalProgressCount = get_total_global_progress_count(state.inputs.selectedDraftOptions)
    state.outputs.currentProgressCount = 0
    JobUtil.new_job_to_firebase(state)

    try :
        # 모든 BoundedContext들에 대해 반복
        for context_name, context in state.inputs.selectedDraftOptions.items():
            bc_name = context.get("boundedContext", {}).get("name", "")
            
            # BoundedContext가 존재하는지 확인
            bounded_context_exists = False
            for element in state.outputs.esValue.elements.values():
                if (element.get("_type") == "org.uengine.modeling.model.BoundedContext" and 
                    element.get("name", "").lower() == bc_name.lower()):
                    bounded_context_exists = True
                    break
            
            # 존재하지 않으면 생성
            if not bounded_context_exists and bc_name:
                # ActionModel을 생성하여 BoundedContext 생성
                actions = [
                    ActionModel(
                        objectType="BoundedContext",
                        type="create",
                        ids={
                            "boundedContextId": context.get("boundedContext", {}).get("id", "")
                        },
                        args={
                            "boundedContextName": bc_name,
                            "boundedContextAlias": context.get("boundedContext", {}).get("displayName", ""),
                            "description": context.get("boundedContext", {}).get("description", "")
                        }
                    )
                ]
                
                # 액션 적용하여 새로운 esValue 생성
                user_info = state.inputs.userInfo.model_dump() if state.inputs.userInfo else {}
                information = state.inputs.information.model_dump() if state.inputs.information else {}
                
                updated_es_value = EsActionsUtil.apply_actions(
                    state.outputs.esValue, 
                    actions, 
                    user_info, 
                    information
                )
                
                # 상태 업데이트
                state.outputs.esValue = updated_es_value
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"Error creating bounded contexts", e)
        return "complete"

    LogUtil.add_info_log(state, "Creating bounded contexts completed")
    state.outputs.currentProgressCount = state.outputs.currentProgressCount + 1
    JobUtil.update_job_to_firebase(state)
    return state

def route_after_create_aggregates(state: State):
    if state.subgraphs.createAggregateByFunctionsModel.is_failed:
        return "complete"

    return "create_class_id" 

def route_after_create_class_id(state: State):
    if state.subgraphs.createAggregateClassIdByDraftsModel.is_failed:
        return "complete"
    
    return "create_command_actions"

def route_after_create_command_actions(state: State):
    if state.subgraphs.createCommandActionsByFunctionModel.is_failed:
        return "complete"
    
    return "create_policy_actions"

def route_after_create_policy_actions(state: State):
    if state.subgraphs.createPolicyActionsByFunctionModel.is_failed:
        return "complete"
    
    return "create_gwt"

def route_after_create_gwt(state: State):
    if state.subgraphs.createGwtGeneratorByFunctionModel.is_failed:
        return "complete"
    
    return "complete"

def complete(state: State):
    state.outputs.isCompleted = True
    JobUtil.update_job_to_firebase(state)

    return state

def get_total_global_progress_count(draftOptions: Dict[str, Any]):
    boundedContextCount = len(draftOptions)

    aggregateCount = 0
    for context in draftOptions.values():
        aggregateCount += len(context.get("structure", []))

    aggregateClassIDCount = _get_total_class_id_progress_count(draftOptions)

    return boundedContextCount + aggregateCount*3 + aggregateClassIDCount + 1

def _get_total_class_id_progress_count(draft_options: Dict[str, Any]):
    total_progress_count = 0

    draft_options = {k: v.get("structure", []) for k, v in draft_options.items()}
 
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
    
    # 처리할 참조 목록 초기화
    if references:
        processed_pairs = set()
        
        for ref in references:
            # 양방향 참조를 한 쌍으로 처리하기 위해 정렬된 키 생성
            pair_key = "-".join(sorted([ref["fromAggregate"], ref["toAggregate"]]))
            
            if pair_key not in processed_pairs:
                processed_pairs.add(pair_key)
                total_progress_count += 1
    
    return total_progress_count

graph_builder = StateGraph(State)

graph_builder.add_node("validate_input", validate_input)
graph_builder.add_node("create_bounded_contexts", create_bounded_contexts)
graph_builder.add_node("create_aggregates", create_aggregate_by_functions_subgraph())
graph_builder.add_node("create_class_id", create_aggregate_class_id_by_drafts_subgraph())
graph_builder.add_node("create_command_actions", create_command_actions_by_function_subgraph())
graph_builder.add_node("create_policy_actions", create_policy_actions_by_function_subgraph())
graph_builder.add_node("create_gwt", create_gwt_generator_by_function_subgraph())
graph_builder.add_node("complete", complete)

graph_builder.add_edge(START, "create_bounded_contexts")
graph_builder.add_edge("create_bounded_contexts", "create_aggregates")
graph_builder.add_conditional_edges("create_aggregates", route_after_create_aggregates, {
    "create_class_id": "create_class_id",
    "complete": "complete"
})
graph_builder.add_conditional_edges("create_class_id", route_after_create_class_id, {
    "create_command_actions": "create_command_actions",
    "complete": "complete"
})
graph_builder.add_conditional_edges("create_command_actions", route_after_create_command_actions, {
    "create_policy_actions": "create_policy_actions",
    "complete": "complete"
})
graph_builder.add_conditional_edges("create_policy_actions", route_after_create_policy_actions, {
    "create_gwt": "create_gwt",
    "complete": "complete"
})
graph_builder.add_conditional_edges("create_gwt", route_after_create_gwt, {
    "complete": "complete"
})

graph = graph_builder.compile()