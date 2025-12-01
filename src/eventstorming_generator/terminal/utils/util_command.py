from .clear_jobs import clear_jobs

util_command_registry = {
    "clearJobs": {
        "handler": clear_jobs,
        "description": "특정 NameSpace에 있는 jobs, jobStates, requestedJobs 폴더를 모두 삭제",
        "usage": "util clearJobs <NameSpace>"
    }
}

def util_command(command_name, command_args):
    util = util_command_registry.get(command_name, None)
    if not util:
        print(f"유효하지 않은 유틸리티 명령어입니다. {command_name}")
        return False
    return util["handler"](command_args)