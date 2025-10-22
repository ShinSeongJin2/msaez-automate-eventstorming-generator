from .graph.run_graph import run_graph
from .generator.run_generator import run_generator
from .util.run_util import run_util

run_command_registry = {
    "runGraph": {
        "handler": run_graph,
        "description": "특정 Graph를 즉시 실행",
        "usage": "run runGraph <Graph 이름>"
    },
    "runGenerator": {
        "handler": run_generator,
        "description": "특정 Generator를 즉시 실행",
        "usage": "run runGenerator <Generator 이름>"
    },
    "runUtil": {
        "handler": run_util,
        "description": "특정 Util를 즉시 실행",
        "usage": "run runUtil <Util 이름>"
    }
}

def run_command(command_name, command_args):
    command = run_command_registry.get(command_name, None)
    if not command:
        print(f"유효하지 않은 콘솔 명령어입니다. {command_name}")
        return False
    return command["handler"](command_args)