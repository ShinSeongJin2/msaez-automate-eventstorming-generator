from ...mocks import aggregate_worker_subgraph_inputs
from .....subgraphs import create_aggregate_worker_subgraph, aggregate_worker_id_context
from .....models import State

def execute_aggregate_worker_subgraph():
    worker_id = '43323970-c478-44ee-9800-0616e1ac9134'

    run_subgraph = create_aggregate_worker_subgraph()
    aggregate_worker_id_context.set(worker_id)
    state: State = run_subgraph(aggregate_worker_subgraph_inputs)

    completed_aggregate = state.subgraphs.createAggregateByFunctionsModel.worker_generations.get(worker_id)
    return {
        "state": state,
        "completed_aggregate": completed_aggregate
    }