from ...mocks import bounded_context_worker_subgraph_inputs
from .....subgraphs import create_bounded_context_worker_subgraph, bounded_context_worker_id_context
from .....models import State

def execute_bounded_context_worker_subgraph():
    worker_id = 'c9ca7e93-421a-469d-a334-e0aecdcd726d'

    run_subgraph = create_bounded_context_worker_subgraph()
    bounded_context_worker_id_context.set(worker_id)
    state: State = run_subgraph(bounded_context_worker_subgraph_inputs)

    completed_bounded_context = state.subgraphs.createBoundedContextByFunctionsModel.worker_generations.get(worker_id)
    return {
        "state": state,
        "completed_bounded_context": completed_bounded_context
    }