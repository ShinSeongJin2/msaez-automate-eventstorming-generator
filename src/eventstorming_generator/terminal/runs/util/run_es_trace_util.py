from eventstorming_generator.terminal.terminal_helper import TerminalHelper
from ....utils import LoggingUtil, ListUtil, EsTraceUtil
from ..mocks import es_trace_util_inputs
from ....models import State

run_name = "run_es_trace_util"
def run_es_trace_util(command_args):
    func_name = ListUtil.get_safely(command_args, 1, None)

    func_dic = {
        "convertRefsToIndexes": run_convert_refs_to_indexes,
    }
    func = func_dic.get(func_name, None)
    if not func:
        LoggingUtil.error(run_name, f"유효하지 않은 함수 이름: {func_name}")
        return False
    
    return func(command_args)

def run_convert_refs_to_indexes(command_args):
    mock_inputs = es_trace_util_inputs["convert_refs_to_indexes"]
    copied_actions = [action.model_copy(deep=True) for action in mock_inputs["actions"]]
    state = State()

    EsTraceUtil.convert_refs_to_indexes(
        copied_actions, 
        mock_inputs["original_description"], 
        mock_inputs["requirement_index_mapping"],
        state, 
        mock_inputs["log_prefix"]
    )

    TerminalHelper.save_dict_to_temp_file({
        "result_actions": copied_actions,
        "logs": state.outputs.logs,
    }, f"{run_name}_state")