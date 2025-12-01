from typing import Optional, Callable
from dataclasses import fields

from ..mocks import input_states
from ....graph import graph
from ....utils.job_utils import JobUtil
from ....models import State
from ....constants import RESUME_NODES, RootGraphNode

def execute_main_graph_sequentially(
        request_type: str="fromRequirements", requirements_type: str="library_requirements", 
        until_after_stop_node: str="none", node_stop_callback: Callable[[str, State], None]=None
    ) -> State:
    root_graph_nodes_to_exclude = ["CREATE_BOUNDED_CONTEXTS_TO_ES_VALUE", "COMPLETE"]
    if request_type == "fromDraft":
        root_graph_nodes_to_exclude.extend([
            "CREATE_BOUNDED_CONTEXTS", "CREATE_CONTEXT_MAPPING", "CREATE_DRAFT_BY_FUNCTION"
        ])

    input_state: Optional[State] = input_states.get(request_type, {}).get(requirements_type, None)
    if not input_state:
        raise ValueError(f"Invalid request type: {request_type}")
    
    previous_state: State = input_state
    root_graph_nodes = [getattr(RESUME_NODES.ROOT_GRAPH, field.name) for field in fields(RootGraphNode) if field.name not in root_graph_nodes_to_exclude]
    for after_stop_node in root_graph_nodes:
        previous_state.inputs.after_stop_node = after_stop_node
        current_state = execute_main_graph(previous_state.model_copy(deep=True))
        
        if node_stop_callback:
            node_stop_callback(after_stop_node, previous_state, current_state)
        if after_stop_node == until_after_stop_node:
            break
        previous_state = current_state
    
    return current_state

def execute_main_graph(state: State) -> State:
    result_state = State(**graph.invoke(state, {"recursion_limit": 2147483647}))
    JobUtil.cleanup_job_resources(result_state.inputs.jobId)
    return result_state