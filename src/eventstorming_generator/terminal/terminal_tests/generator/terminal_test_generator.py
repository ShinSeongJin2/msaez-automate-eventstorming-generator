import os

terminal_test_generator_registry = {
    "CreateBoundedContextGenerator": {
        "handler": lambda command_args: os.system("uv run pytest tests/generators/test_create_bounded_context_generator.py -v"),
        "description": "CreateBoundedContextGenerator 테스트",
        "usage": "test testGenerator CreateBoundedContextGenerator"
    },
    "MergeCreatedBoundedContextGenerator": {
        "handler": lambda command_args: os.system("uv run pytest tests/generators/test_merge_created_bounded_context_generator.py -v"),
        "description": "MergeCreatedBoundedContextGenerator 테스트",
        "usage": "test testGenerator MergeCreatedBoundedContextGenerator"
    },
    "RequirementMappingGenerator": {
        "handler": lambda command_args: os.system("uv run pytest tests/generators/test_requirement_mapping_generator.py -v"),
        "description": "RequirementMappingGenerator 테스트",
        "usage": "test testGenerator RequirementMappingGenerator"
    },
    "CreateDraftGenerator": {
        "handler": lambda command_args: os.system("uv run pytest tests/generators/test_create_draft_generator.py -v"),
        "description": "CreateDraftGenerator 테스트",
        "usage": "test testGenerator CreateDraftGenerator"
    },
    "MergeDraftGenerator": {
        "handler": lambda command_args: os.system("uv run pytest tests/generators/test_merge_draft_generator.py -v"),
        "description": "MergeDraftGenerator 테스트",
        "usage": "test testGenerator MergeDraftGenerator"
    },
    "CreateAggregateActionsByFunction": {
        "handler": lambda command_args: os.system("uv run pytest tests/generators/test_create_aggregate_actions_by_function.py -v"),
        "description": "CreateAggregateActionsByFunction 테스트",
        "usage": "test testGenerator CreateAggregateActionsByFunction"
    },
    "AssignFieldsToActionsGenerator": {
        "handler": lambda command_args: os.system("uv run pytest tests/generators/test_assign_fields_to_actions_generator.py -v"),
        "description": "AssignFieldsToActionsGenerator 테스트",
        "usage": "test testGenerator AssignFieldsToActionsGenerator"
    }
}

def terminal_test_generator(command_args):
    test_generator_name = command_args[0]

    test_generator = terminal_test_generator_registry.get(test_generator_name, None)
    if not test_generator:
        print(f"유효하지 않은 제너레이터 명령어입니다. {test_generator_name}")
        return False
    return test_generator["handler"](command_args)