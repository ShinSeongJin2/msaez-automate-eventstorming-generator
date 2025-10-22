import time

from ..mocks import input_state
from ....graph import graph
from ...terminal_util import TerminalUtil
from ....utils import LoggingUtil
from ....models import State

def run_main_graph(command_args):
    run_name = "run_main_graph"

    try:
        
        start_time = time.time()
        result = State(**graph.invoke(input_state, {"recursion_limit": 2147483647}))
        end_time = time.time()
        total_seconds = end_time - start_time
        
        TerminalUtil.save_dict_to_temp_file({
            "esValue": result.outputs.esValue,
            "logs": result.outputs.logs,
            "totalSeconds": total_seconds
        }, run_name)
        TerminalUtil.save_es_summarize_result_to_temp_file(result.outputs.esValue, run_name)
        TerminalUtil.check_error_logs_from_state(result, run_name)

    except Exception as e:
        LoggingUtil.exception(run_name, f"실행 실패", e)
        TerminalUtil.save_dict_to_temp_file({
            "error": str(e),
            "input_state": input_state
        }, f"{run_name}_error")
        raise
