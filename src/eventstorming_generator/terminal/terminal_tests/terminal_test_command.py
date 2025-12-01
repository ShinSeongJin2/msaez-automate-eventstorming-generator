import os

from .sub_graph.terminal_test_sub_graph import terminal_test_sub_graph
from .worker_subgraph.terminal_test_worker_subgraph import terminal_test_worker_subgraph
from .sub_graph_util.terminal_test_sub_graph_util import terminal_test_sub_graph_util
from .generator_util.terminal_test_generator_util import terminal_test_generator_util
from .generator.terminal_test_generator import terminal_test_generator
from .util.terminal_test_util import terminal_test_util

terminal_test_command_registry = {
    "all": {
        "handler": lambda command_args: os.system("uv run pytest -v"),
        "description": "모든 테스트 실행",
        "usage": "test all"
    },
    "testMainGraph": {
        "handler": lambda command_args: os.system("uv run pytest -v tests/graphs/test_main_graph.py"),
        "description": "MainGraph 테스트",
        "usage": "test testMainGraph"
    },
    "testSubGraph": {
        "handler": terminal_test_sub_graph,
        "description": "특정 서브그래프를 테스트",
        "usage": "test testSubGraph <서브그래프 이름>"
    },
    "testWorkerSubgraph": {
        "handler": terminal_test_worker_subgraph,
        "description": "특정 워커 서브그래프를 테스트",
        "usage": "test testWorkerSubgraph <워커 서브그래프 이름>"
    },
    "testSubGraphUtil": {
        "handler": terminal_test_sub_graph_util,
        "description": "특정 서브그래프 유틸리티를 테스트",
        "usage": "test testSubGraphUtil <서브그래프 유틸리티 이름>"
    },
    "testGeneratorUtil": {
        "handler": terminal_test_generator_util,
        "description": "특정 제너레이터 유틸리티를 테스트",
        "usage": "test testGeneratorUtil <제너레이터 유틸리티 이름>"
    },
    "testGenerator": {
        "handler": terminal_test_generator,
        "description": "특정 제너레이터를 테스트",
        "usage": "test testGenerator <제너레이터 이름>"
    },
    "testUtil": {
        "handler": terminal_test_util,
        "description": "특정 Util를 테스트",
        "usage": "test testUtil <Util 이름>"
    }
}

def terminal_test_command(command_name, command_args):
    command = terminal_test_command_registry.get(command_name, None)
    if not command:
        print(f"유효하지 않은 콘솔 명령어입니다. {command_name}")
        return False
    return command["handler"](command_args)