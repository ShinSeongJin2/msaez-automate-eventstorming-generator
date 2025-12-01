from ...mocks import draft_worker_subgraph_inputs
from .....subgraphs import create_draft_worker_subgraph, draft_worker_id_context
from .....models import State

def execute_draft_worker_subgraph():
    worker_id = '976547bb-d41d-4283-ba54-bda3de9fef93'

    run_subgraph = create_draft_worker_subgraph()
    draft_worker_id_context.set(worker_id)
    state: State = run_subgraph(draft_worker_subgraph_inputs)

    completed_draft = state.subgraphs.createDraftByFunctionModel.worker_generations.get(worker_id)
    return {
        "state": state,
        "completed_draft": completed_draft
    }