from ..mocks import create_context_mapping_sub_graph_inputs
from ....subgraphs import create_context_mapping_subgraph
from ....utils.job_utils import JobUtil
from ....models import State

def execute_create_context_mapping_sub_graph() -> State:
    run_subgraph = create_context_mapping_subgraph()
    state: State = run_subgraph(create_context_mapping_sub_graph_inputs.model_copy(deep=True))
    JobUtil.cleanup_job_resources(state.inputs.jobId)
    return state