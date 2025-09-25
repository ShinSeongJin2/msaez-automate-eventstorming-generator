from ..mocks import create_command_actions_by_function_sub_graph_inputs
from ...subgraphs import create_command_actions_by_function_subgraph
from ..run_util import RunUtil
from ...utils import LoggingUtil
from ...models import State

def run_create_command_actions_by_function_sub_graph():
    run_name = "run_create_command_actions_by_function_sub_graph"

    try:

        run_subgraph = create_command_actions_by_function_subgraph()
        result: State = run_subgraph(create_command_actions_by_function_sub_graph_inputs)
        RunUtil.save_dict_to_temp_file({
            "esValue": result.outputs.esValue,
            "logs": result.outputs.logs,
            "totalSeconds": result.subgraphs.createCommandActionsByFunctionModel.total_seconds
        }, run_name)
        RunUtil.save_es_summarize_result_to_temp_file(result.outputs.esValue, run_name)
        RunUtil.check_error_logs_from_state(result, run_name)
        
    except Exception as e:
        LoggingUtil.exception(run_name, f"실행 실패", e)
        RunUtil.save_dict_to_temp_file({
            "error": str(e)
        }, f"{run_name}_error")
        raise
