from ....utils import LoggingUtil, ListUtil
from ...terminal_helper import TerminalHelper
from ...commons.util import execute_text_chunker_util

run_name = "run_text_chunker_util"
def run_text_chunker_util(command_args):
    func_name = ListUtil.get_safely(command_args, 1, None)

    func_dic = {
        "splitIntoChunksByLine": run_split_into_chunks_by_line,
    }
    func = func_dic.get(func_name, None)
    if not func:
        LoggingUtil.error(run_name, f"유효하지 않은 함수 이름: {func_name}")
        return False
    
    return func(command_args)

def run_split_into_chunks_by_line(command_args):
    chunks = execute_text_chunker_util()
    TerminalHelper.save_dict_to_temp_file(chunks, f"{run_name}_chunks")