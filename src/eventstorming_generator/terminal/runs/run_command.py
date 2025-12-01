from .graph.run_graph import run_graph
from .sub_graph_util.run_sub_graph_util import run_sub_graph_util
from .generator_util.run_generator_util import run_generator_util
from .generator.run_generator import run_generator
from .util.run_util import run_util
from .a2a.run_a2a import run_a2a
from .util.run_es_trace_util import run_es_trace_util

run_command_registry = {
    "runGraph": {
        "handler": run_graph,
        "description": "특정 Graph를 즉시 실행",
        "usage": "run runGraph <Graph 이름>"
    },
    "runSubGraphUtil": {
        "handler": run_sub_graph_util,
        "description": "특정 SubGraphUtil를 즉시 실행",
        "usage": "run runSubGraphUtil <SubGraphUtil 이름>"
    },
    "runGeneratorUtil": {
        "handler": run_generator_util,
        "description": "특정 GeneratorUtil를 즉시 실행",
        "usage": "run runGeneratorUtil <GeneratorUtil 이름>"
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
    },
    "runA2A": {
        "handler": run_a2a,
        "description": "특정 A2A 관련 커멘드를 실행",
        "usage": "run runA2A <A2A 커멘드 이름>"
    },
    "runEsTraceUtil": {
        "handler": run_es_trace_util,
        "description": "EsTraceUtil 유틸리티를 즉시 실행",
        "usage": "run runEsTraceUtil <convertRefsToIndexes>"
    }
}

def run_command(command_name, command_args):
    command = run_command_registry.get(command_name, None)
    if not command:
        print(f"유효하지 않은 콘솔 명령어입니다. {command_name}")
        return False
    return command["handler"](command_args)