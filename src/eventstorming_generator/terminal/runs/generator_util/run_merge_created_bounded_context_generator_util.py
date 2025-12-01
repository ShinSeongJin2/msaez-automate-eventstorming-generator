from ....utils import LoggingUtil, ListUtil
from ...terminal_helper import TerminalHelper
from ...commons.generator_util import execute_merge_created_bounded_context_safely

run_name = "run_merge_created_bounded_context_generator_util"
def run_merge_created_bounded_context_generator_util(command_args):
    func_name = ListUtil.get_safely(command_args, 1, None)
    func_dic = {
        "mergeCreatedBoundedContextSafely": run_merge_created_bounded_context_safely,
    }
    func = func_dic.get(func_name, None)
    if not func:
        LoggingUtil.error(run_name, f"유효하지 않은 함수 이름: {func_name}")
        return False
    
    return func(command_args)

def run_merge_created_bounded_context_safely(command_args):
    bounded_context_infos = execute_merge_created_bounded_context_safely()
    TerminalHelper.save_dict_to_temp_file(bounded_context_infos, f"run_merge_created_bounded_context_safely_bounded_context_infos")
    return True