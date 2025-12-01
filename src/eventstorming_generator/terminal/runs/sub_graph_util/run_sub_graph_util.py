from .run_create_context_mapping_util import run_create_context_mapping_util

run_sub_graph_util_registry = {
    "CreateContextMappingUtil": {
        "handler": run_create_context_mapping_util,
        "description": "CreateContextMappingUtil 유틸리티를 즉시 실행",
        "usage": "run runSubGraphUtil CreateContextMappingUtil <getReferencedContextMappings>"
    }
}

def run_sub_graph_util(command_args):
    sub_graph_util_name = command_args[0]

    sub_graph_util = run_sub_graph_util_registry.get(sub_graph_util_name, None)
    if not sub_graph_util:
        print(f"유효하지 않은 서브그래프 유틸리티 명령어입니다. {sub_graph_util_name}")
        return False
    return sub_graph_util["handler"](command_args)