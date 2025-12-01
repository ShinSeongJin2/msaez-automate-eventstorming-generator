import os

terminal_test_sub_graph_registry = {
    "CreateBoundedContextByFunctionsSubGraph": {
        "handler": lambda command_args: os.system("uv run pytest tests/sub_graphs/test_create_bounded_context_by_functions_sub_graph.py -v"),
        "description": "CreateBoundedContextByFunctionsSubGraph 테스트",
        "usage": "test testSubGraph CreateBoundedContextByFunctionsSubGraph"
    },
    "CreateContextMappingSubGraph": {
        "handler": lambda command_args: os.system("uv run pytest tests/sub_graphs/test_create_context_mapping_sub_graph.py -v"),
        "description": "CreateContextMappingSubGraph 테스트",
        "usage": "test testSubGraph CreateContextMappingSubGraph"
    },
    "CreateDraftByFunctionSubGraph": {
        "handler": lambda command_args: os.system("uv run pytest tests/sub_graphs/test_create_draft_by_function_sub_graph.py -v"),
        "description": "CreateDraftByFunctionSubGraph 테스트",
        "usage": "test testSubGraph CreateDraftByFunctionSubGraph"
    },
    "CreateAggregateByFunctionsSubGraph": {
        "handler": lambda command_args: os.system("uv run pytest tests/sub_graphs/test_create_aggregate_by_functions_sub_graph.py -v"),
        "description": "CreateAggregateByFunctionsSubGraph 테스트",
        "usage": "test testSubGraph CreateAggregateByFunctionsSubGraph"
    },
    "CreateCommandActionsByFunctionSubGraph": {
        "handler": lambda command_args: os.system("uv run pytest tests/sub_graphs/test_create_command_actions_by_function_sub_graph.py -v"),
        "description": "CreateCommandActionsByFunctionSubGraph 테스트",
        "usage": "test testSubGraph CreateCommandActionsByFunctionSubGraph"
    },
    "CreatePolicyActionsByFunctionSubGraph": {
        "handler": lambda command_args: os.system("uv run pytest tests/sub_graphs/test_create_policy_actions_by_function_sub_graph.py -v"),
        "description": "CreatePolicyActionsByFunctionSubGraph 테스트",
        "usage": "test testSubGraph CreatePolicyActionsByFunctionSubGraph"
    },
}

def terminal_test_sub_graph(command_args):
    test_sub_graph_name = command_args[0]

    test_sub_graph = terminal_test_sub_graph_registry.get(test_sub_graph_name, None)
    if not test_sub_graph:
        print(f"유효하지 않은 서브그래프 명령어입니다. {test_sub_graph_name}")
        return False
    return test_sub_graph["handler"](command_args)