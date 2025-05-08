from langgraph.graph import StateGraph, START, END

from eventstorming_generator.models import InputsModel, OutputsModel, BaseModelWithItem, ActionModel
from eventstorming_generator.utils import EsActionsUtil

class State(BaseModelWithItem):
    inputs: InputsModel = InputsModel()
    outputs: OutputsModel = OutputsModel()

def create_bounded_contexts(state: State):
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
                        "boundedContextId": f"bc-{bc_name}"
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
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("create_bounded_contexts", create_bounded_contexts)

graph_builder.add_edge(START, "create_bounded_contexts")
graph_builder.add_edge("create_bounded_contexts", END)
graph = graph_builder.compile()