from ..mocks import create_element_names_by_draft_sub_graph_inputs
from ...subgraphs import create_element_names_by_draft_sub_graph
from ..run_util import RunUtil
from ...utils import LoggingUtil
from ...models import State

def run_create_element_names_by_draft_sub_graph():
    run_name = "run_create_element_names_by_draft_sub_graph"

    try:

        run_subgraph = create_element_names_by_draft_sub_graph()
        result: State = run_subgraph(create_element_names_by_draft_sub_graph_inputs)
        RunUtil.save_dict_to_temp_file({
            "extracted_element_names": result.subgraphs.createElementNamesByDraftsModel.extracted_element_names,
            "logs": result.outputs.logs,
            "totalSeconds": result.subgraphs.createElementNamesByDraftsModel.total_seconds
        }, run_name)
        RunUtil.check_error_logs_from_state(result, run_name)
        
    except Exception as e:
        LoggingUtil.exception(run_name, f"실행 실패", e)
        RunUtil.save_dict_to_temp_file({
            "error": str(e)
        }, f"{run_name}_error")
        raise
