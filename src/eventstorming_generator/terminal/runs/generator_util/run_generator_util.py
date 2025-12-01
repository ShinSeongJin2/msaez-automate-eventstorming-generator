from .run_merge_created_bounded_context_generator_util import run_merge_created_bounded_context_generator_util
from .run_create_draft_generator_util import run_create_draft_generator_util
from .run_merge_draft_generator_util import run_merge_draft_generator_util

run_generator_util_registry = {
    "MergeCreatedBoundedContextGeneratorUtil": {
        "handler": run_merge_created_bounded_context_generator_util,
        "description": "MergeCreatedBoundedContextGeneratorUtil 유틸리티를 즉시 실행",
        "usage": "run runGeneratorUtil MergeCreatedBoundedContextGeneratorUtil <mergeCreatedBoundedContextSafely>"
    },
    "CreateDraftGeneratorUtil": {
        "handler": run_create_draft_generator_util,
        "description": "CreateDraftGeneratorUtil 유틸리티를 즉시 실행",
        "usage": "run runGeneratorUtil CreateDraftGeneratorUtil <createDraftByFunctionSafely>"
    },
    "MergeDraftGeneratorUtil": {
        "handler": run_merge_draft_generator_util,
        "description": "MergeDraftGeneratorUtil 유틸리티를 즉시 실행",
        "usage": "run runGeneratorUtil MergeDraftGeneratorUtil <sequentialMergeDraftsSafely>"
    }
}

def run_generator_util(command_args):
    generator_util_name = command_args[0]

    generator_util = run_generator_util_registry.get(generator_util_name, None)
    if not generator_util:
        print(f"유효하지 않은 제너레이터 유틸리티 명령어입니다. {generator_util_name}")
        return False
    return generator_util["handler"](command_args)