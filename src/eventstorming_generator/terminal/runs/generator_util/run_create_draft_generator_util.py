from ....utils import LoggingUtil, ListUtil
from ...terminal_helper import TerminalHelper
from ...commons.generator_util import execute_create_draft_by_function_safely

run_name = "run_create_draft_generator_util"
def run_create_draft_generator_util(command_args):
    func_name = ListUtil.get_safely(command_args, 1, None)
    func_dic = {
        "createDraftByFunctionSafely": run_create_draft_by_function_safely,
    }
    func = func_dic.get(func_name, None)
    if not func:
        LoggingUtil.error(run_name, f"유효하지 않은 함수 이름: {func_name}")
        return False
    
    return func(command_args)

def run_create_draft_by_function_safely(command_args):
    draft = execute_create_draft_by_function_safely()
    TerminalHelper.save_dict_to_temp_file(draft, f"run_create_draft_by_function_safely_draft")
    return True