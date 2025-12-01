from ..mocks import create_draft_by_function_sub_graph_inputs
from ....subgraphs import create_draft_by_function_subgraph
from ....utils.job_utils import JobUtil
from ....models import State

def execute_create_draft_by_function_sub_graph() -> State:
    run_subgraph = create_draft_by_function_subgraph()
    state: State = run_subgraph(create_draft_by_function_sub_graph_inputs.model_copy(deep=True))
    JobUtil.cleanup_job_resources(state.inputs.jobId)
    return state