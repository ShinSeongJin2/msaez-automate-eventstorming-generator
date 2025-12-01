import asyncio

from .request_requirements_to_a2a_server import request_requirements_to_a2a_server

run_a2a_registry = {
    "requestRequirementsToA2AServer": {
        "handler": request_requirements_to_a2a_server,
        "description": "실행된 A2A 서버에 요구사항을 전달하고, 실시간으로 결과를 스트리밍",
        "usage": "run runA2A requestRequirementsToA2AServer"
    }
}

def run_a2a(command_args):
    a2a_name = command_args[0]

    a2a = run_a2a_registry.get(a2a_name, None)
    if not a2a:
        print(f"유효하지 않은 A2A 명령어입니다. {a2a_name}")
        return False
    return asyncio.run(a2a["handler"](command_args))