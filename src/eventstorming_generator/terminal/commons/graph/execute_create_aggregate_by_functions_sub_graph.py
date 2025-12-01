from ..mocks import create_aggregate_by_functions_sub_graph_inputs
from ....subgraphs import create_aggregate_by_functions_subgraph
from ....utils.job_utils import JobUtil
from ....models import State

def execute_create_aggregate_by_functions_sub_graph() -> State:
    run_subgraph = create_aggregate_by_functions_subgraph()
    state: State = run_subgraph(create_aggregate_by_functions_sub_graph_inputs.model_copy(deep=True))
    JobUtil.cleanup_job_resources(state.inputs.jobId)
    return state