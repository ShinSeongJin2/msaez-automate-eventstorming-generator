from ....utils import LoggingUtil, ListUtil
from ...terminal_helper import TerminalHelper
from ...commons.generator_util import execute_sequential_merge_drafts_safely

run_name = "run_merge_draft_generator_util"
def run_merge_draft_generator_util(command_args):
    func_name = ListUtil.get_safely(command_args, 1, None)
    func_dic = {
        "sequentialMergeDraftsSafely": run_sequential_merge_drafts_safely,
    }
    func = func_dic.get(func_name, None)
    if not func:
        LoggingUtil.error(run_name, f"유효하지 않은 함수 이름: {func_name}")
        return False
    
    return func(command_args)

def run_sequential_merge_drafts_safely(command_args):
    merged_drafts = execute_sequential_merge_drafts_safely()
    TerminalHelper.save_dict_to_temp_file(merged_drafts, f"run_sequential_merge_drafts_safely_merged_drafts")
    return True