import os

terminal_test_generator_util_registry = {
    "MergeCreatedBoundedContextGeneratorUtil": {
        "handler": lambda command_args: os.system("uv run pytest tests/generator_utils/test_merge_created_bounded_context_generator_util.py -v"),
        "description": "MergeCreatedBoundedContextGeneratorUtil 테스트",
        "usage": "test testGeneratorUtil MergeCreatedBoundedContextGeneratorUtil"
    },
    "CreateDraftGeneratorUtil": {
        "handler": lambda command_args: os.system("uv run pytest tests/generator_utils/test_create_draft_generator_util.py -v"),
        "description": "CreateDraftGeneratorUtil 테스트",
        "usage": "test testGeneratorUtil CreateDraftGeneratorUtil"
    },
    "MergeDraftGeneratorUtil": {
        "handler": lambda command_args: os.system("uv run pytest tests/generator_utils/test_merge_draft_generator_util.py -v"),
        "description": "MergeDraftGeneratorUtil 테스트",
        "usage": "test testGeneratorUtil MergeDraftGeneratorUtil"
    }
}

def terminal_test_generator_util(command_args):
    test_generator_util_name = command_args[0]

    test_generator_util = terminal_test_generator_util_registry.get(test_generator_util_name, None)
    if not test_generator_util  :
        print(f"유효하지 않은 제너레이터 유틸리티 명령어입니다. {test_generator_util_name}")
        return False
    return test_generator_util["handler"](command_args)