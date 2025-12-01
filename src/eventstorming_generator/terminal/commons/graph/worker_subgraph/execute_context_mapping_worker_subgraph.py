from ...mocks import context_mapping_worker_subgraph_inputs
from .....subgraphs import create_context_mapping_worker_subgraph, context_mapping_worker_id_context
from .....models import State

def execute_context_mapping_worker_subgraph():
    worker_id = 'c259c519-ce65-4afe-951f-f77cb8189f9b'

    run_subgraph = create_context_mapping_worker_subgraph()
    context_mapping_worker_id_context.set(worker_id)
    state: State = run_subgraph(context_mapping_worker_subgraph_inputs)

    completed_context_mapping = state.subgraphs.createContextMappingModel.worker_generations.get(worker_id)
    return {
        "state": state,
        "completed_context_mapping": completed_context_mapping
    }