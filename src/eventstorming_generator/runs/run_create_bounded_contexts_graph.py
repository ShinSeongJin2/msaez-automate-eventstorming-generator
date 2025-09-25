from .mocks import input_state
from ..graph import create_bounded_contexts
from .run_util import RunUtil
from ..utils import LoggingUtil

def run_create_bounded_contexts_graph():
    run_name = "run_create_bounded_contexts_graph"

    try:

        result = create_bounded_contexts(input_state)
        RunUtil.save_dict_to_temp_file(result, run_name)
        RunUtil.save_es_summarize_result_to_temp_file(result.outputs.esValue, run_name)

    except Exception as e:
        LoggingUtil.exception(run_name, f"실행 실패", e)
        RunUtil.save_dict_to_temp_file({
            "error": str(e),
            "input_state": input_state
        }, f"{run_name}_error")
        raise
