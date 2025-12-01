from ..runs.run_command import run_command_registry
from ..runs.graph.run_graph import run_graph_registry
from ..runs.graph.sub_graph.run_sub_graph import run_sub_graph_registry
from ..runs.graph.worker_subgraph.run_worker_sub_graph import run_worker_sub_graph_registry
from ..runs.sub_graph_util.run_sub_graph_util import run_sub_graph_util_registry
from ..runs.generator_util.run_generator_util import run_generator_util_registry
from ..runs.generator.run_generator import run_generator_registry
from ..runs.util.run_util import run_util_registry
from ..runs.a2a.run_a2a import run_a2a_registry

from ..terminal_tests.terminal_test_command import terminal_test_command_registry
from ..terminal_tests.sub_graph.terminal_test_sub_graph import terminal_test_sub_graph_registry
from ..terminal_tests.worker_subgraph.terminal_test_worker_subgraph import terminal_test_worker_subgraph_registry
from ..terminal_tests.sub_graph_util.terminal_test_sub_graph_util import terminal_test_sub_graph_util_registry
from ..terminal_tests.generator_util.terminal_test_generator_util import terminal_test_generator_util_registry
from ..terminal_tests.generator.terminal_test_generator import terminal_test_generator_registry
from ..terminal_tests.util.terminal_test_util import terminal_test_util_registry

from ..utils.util_command import util_command_registry
from ...utils import ListUtil

command_registry = {
    "run": {
        "run": run_command_registry,
        "runGraph": run_graph_registry,
        "runGraph.SubGraph": run_sub_graph_registry,
        "runGraph.WorkerSubGraph": run_worker_sub_graph_registry,
        "runSubGraphUtil": run_sub_graph_util_registry,
        "runGeneratorUtil": run_generator_util_registry,
        "runGenerator": run_generator_registry,
        "runUtil": run_util_registry,
        "runA2A": run_a2a_registry
    },
    "test": {
        "test": terminal_test_command_registry,
        "testSubGraph": terminal_test_sub_graph_registry,
        "testWorkerSubgraph": terminal_test_worker_subgraph_registry,
        "testSubGraphUtil": terminal_test_sub_graph_util_registry,
        "testGeneratorUtil": terminal_test_generator_util_registry,
        "testGenerator": terminal_test_generator_registry,
        "testUtil": terminal_test_util_registry
    },
    "util": {
        "util": util_command_registry
    }
}

def help_command(command_name, command_args):
    search_command_type = command_name
    search_command_title = ListUtil.get_safely(command_args, 0, None)
    
    help_strings = make_help_strings(search_command_type, search_command_title, command_registry)
    help_message = "\n".join(help_strings)

    with open("./terminal_help.md", "w", encoding="utf-8") as f:
        f.write(help_message)
    print(help_message)

def make_help_strings(search_command_type, search_command_title, command_registry):
    help_strings = []

    if search_command_type == "help":
        help_strings.append("# Help Commands")
        help_strings.append("## help: 모든 콘솔 명령어 목록 출력")
        help_strings.append("## help all: 모든 콘솔 명령어 목록 출력")
        help_strings.append("## help <commandType>: 특정 타입의 콘솔 명령어 목록 출력")
        help_strings.append("## help <commandType> <commandTitle>: 특정 타입에 속한 특정 명령어 집합 상세 정보 출력")
        return help_strings

    if search_command_type == "all" or not search_command_type:
        help_strings.append("# All Commands")
        for command_type in command_registry:
            help_strings.append(f"## {command_type}")
            for command_title in command_registry[command_type]:
                help_strings.append(get_command_registry_string(command_title, command_registry[command_type][command_title]))
                help_strings.append("")
            help_strings.append("")
        return help_strings

    if search_command_type and search_command_title:
        if search_command_type in command_registry and search_command_title in command_registry[search_command_type]:
            help_strings.append(get_command_registry_string(search_command_title, command_registry[search_command_type][search_command_title]))
        else:
            help_strings.append(f"유효하지 않은 콘솔 명령어입니다. {search_command_type} {search_command_title}")
        return help_strings

    if search_command_type and not search_command_title:
        if search_command_type in command_registry:
            help_strings.append(f"## {search_command_type}")
            for command_title in command_registry[search_command_type]:
                help_strings.append(get_command_registry_string(command_title, command_registry[search_command_type][command_title]))
                help_strings.append("")
        else:
            help_strings.append(f"유효하지 않은 콘솔 명령어입니다. {search_command_type}")
        return help_strings

    help_strings.append(f"유효하지 않은 콘솔 명령어입니다. {search_command_type} {search_command_title}")
    return help_strings

def get_command_registry_string(title, command_registry):
    help_strings = []
    
    help_strings.append(f"### {title}")
    for command in command_registry.values():
        help_strings.append(f"   - {command['usage']}: {command['description']}")

    return "\n".join(help_strings)