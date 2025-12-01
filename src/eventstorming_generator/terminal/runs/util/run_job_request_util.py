import asyncio

from ....utils import LoggingUtil, ListUtil
from ...commons.util import execute_job_request_util

run_name = "run_job_request_util"
def run_job_request_util(command_args):
    func_name = ListUtil.get_safely(command_args, 1, None)

    func_dic = {
        "addJobRequestByRequirements": run_add_job_request_by_requirements,
    }
    func = func_dic.get(func_name, None)
    if not func:
        LoggingUtil.error(run_name, f"유효하지 않은 함수 이름: {func_name}")
        return False
    
    return asyncio.run(func(command_args))

async def run_add_job_request_by_requirements(command_args):
    requirements_type = ListUtil.get_safely(command_args, 2, "library_requirements")
    await execute_job_request_util(requirements_type)