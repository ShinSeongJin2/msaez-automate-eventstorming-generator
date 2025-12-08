from ....utils import LoggingUtil, ListUtil
from ....utils.job_utils import JobRequirementsUtil
from ..mocks import job_requirements_util_inputs
from ...terminal_helper import TerminalHelper

run_name = "run_job_requirements_util"
def run_job_requirements_util(command_args):
    func_name = ListUtil.get_safely(command_args, 1, None)
    func_dic = {
        "parseRequirements": run_parse_requirements,
    }
    func = func_dic.get(func_name, None)
    if not func:
        LoggingUtil.error(run_name, f"유효하지 않은 함수 이름: {func_name}")
        return False
    
    return func(command_args)

def run_parse_requirements(command_args):
    result = JobRequirementsUtil.parse_requirements(job_requirements_util_inputs.get("parse_requirements"))
    TerminalHelper.save_dict_to_temp_file({
        "result": result
    }, f"{run_name}_result")