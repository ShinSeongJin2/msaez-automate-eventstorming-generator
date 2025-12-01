import os

terminal_test_sub_graph_util_registry = {
    "ContextMappingUtil": {
        "handler": lambda command_args: os.system("uv run pytest tests/sub_graph_utils/test_create_context_mapping_util.py -v"),
        "description": "ContextMappingUtil 테스트",
        "usage": "test testSubGraphUtil ContextMappingUtil"
    },
    "CreateAggregateByFunctionsUtil": {
        "handler": lambda command_args: os.system("uv run pytest tests/sub_graph_utils/test_create_aggregate_by_functions_util.py -v"),
        "description": "CreateAggregateByFunctionsUtil 테스트",
        "usage": "test testSubGraphUtil CreateAggregateByFunctionsUtil"
    }
}

def terminal_test_sub_graph_util(command_args):
    test_sub_graph_util_name = command_args[0]

    test_sub_graph_util = terminal_test_sub_graph_util_registry.get(test_sub_graph_util_name, None)
    if not test_sub_graph_util:
        print(f"유효하지 않은 서브그래프 유틸리티 명령어입니다. {test_sub_graph_util_name}")
        return False
    return test_sub_graph_util["handler"](command_args)