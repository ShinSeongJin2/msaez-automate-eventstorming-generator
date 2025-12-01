from ....utils import LoggingUtil, ListUtil, CreateContextMappingUtil
from ...terminal_helper import TerminalHelper
from ..mocks import create_context_mapping_util_inputs

run_name = "run_create_context_mapping_util"
def run_create_context_mapping_util(command_args):
    func_name = ListUtil.get_safely(command_args, 1, None)
    func_dic = {
        "getReferencedContextMappings": run_get_referenced_context_mappings,
    }
    func = func_dic.get(func_name, None)
    if not func:
        LoggingUtil.error(run_name, f"유효하지 않은 함수 이름: {func_name}")
        return False
    
    return func(command_args)

def run_get_referenced_context_mappings(command_args):
    referenced_context_mappings = CreateContextMappingUtil.get_referenced_context_mappings(
        create_context_mapping_util_inputs["line_number_ranges"], create_context_mapping_util_inputs["requirements"]
    )
    TerminalHelper.save_dict_to_temp_file(
        referenced_context_mappings, f"{run_name}_referenced_context_mappings"
    )