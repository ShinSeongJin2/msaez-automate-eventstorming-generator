from .run_create_bounded_context_by_functions_sub_graph import run_create_bounded_context_by_functions_sub_graph
from .run_create_context_mapping_sub_graph import run_create_context_mapping_sub_graph
from .run_create_draft_by_function_sub_graph import run_create_draft_by_function_sub_graph
from .run_create_aggregate_by_functions_sub_graph import run_create_aggregate_by_functions_sub_graph
from .run_create_aggregate_class_id_by_drafts_sub_graph import run_create_aggregate_class_id_by_drafts_sub_graph
from .run_create_element_names_by_draft_sub_graph import run_create_element_names_by_draft_sub_graph
from .run_create_command_actions_by_function_sub_graph import run_create_command_actions_by_function_sub_graph
from .run_create_policy_actions_by_function_sub_graph import run_create_policy_actions_by_function_sub_graph
from .run_create_gwt_generator_by_function_sub_graph import run_create_gwt_generator_by_function_sub_graph
from .run_create_ui_components_subgraph import run_create_ui_components_subgraph
from .run_es_value_summary_generator_sub_graph import run_es_value_summary_generator_sub_graph

run_sub_graph_registry = {
    "CreateBoundedContextByFunctionsSubGraph": {
        "handler": run_create_bounded_context_by_functions_sub_graph,
        "description": "CreateBoundedContextByFunctionsSubGraph를 즉시 실행",
        "usage": "run runGraph SubGraph CreateBoundedContextByFunctionsSubGraph [<db_type>]"
    },
    "CreateContextMappingSubGraph": {
        "handler": run_create_context_mapping_sub_graph,
        "description": "CreateContextMappingSubGraph를 즉시 실행",
        "usage": "run runGraph SubGraph CreateContextMappingSubGraph [<db_type>]"
    },
    "CreateDraftByFunctionSubGraph": {
        "handler": run_create_draft_by_function_sub_graph,
        "description": "CreateDraftByFunctionSubGraph를 즉시 실행",
        "usage": "run runGraph SubGraph CreateDraftByFunctionSubGraph [<db_type>]"
    },
    "CreateAggregateByFunctionsSubGraph": {
        "handler": run_create_aggregate_by_functions_sub_graph,
        "description": "CreateAggregateByFunctionsSubGraph를 즉시 실행",
        "usage": "run runGraph SubGraph CreateAggregateByFunctionsSubGraph [<db_type>]"
    },
    "CreateAggregateClassIdByDraftsSubGraph": {
        "handler": run_create_aggregate_class_id_by_drafts_sub_graph,
        "description": "CreateAggregateClassIdByDraftsSubGraph를 즉시 실행",
        "usage": "run runGraph SubGraph CreateAggregateClassIdByDraftsSubGraph"
    },
    "CreateElementNamesByDraftSubGraph": {
        "handler": run_create_element_names_by_draft_sub_graph,
        "description": "CreateElementNamesByDraftSubGraph를 즉시 실행",
        "usage": "run runGraph SubGraph CreateElementNamesByDraftSubGraph"
    },
    "CreateCommandActionsByFunctionSubGraph": {
        "handler": run_create_command_actions_by_function_sub_graph,
        "description": "CreateCommandActionsByFunctionSubGraph를 즉시 실행",
        "usage": "run runGraph SubGraph CreateCommandActionsByFunctionSubGraph [<db_type>]"
    },
    "CreatePolicyActionsByFunctionSubGraph": {
        "handler": run_create_policy_actions_by_function_sub_graph,
        "description": "CreatePolicyActionsByFunctionSubGraph를 즉시 실행",
        "usage": "run runGraph SubGraph CreatePolicyActionsByFunctionSubGraph [<db_type>]"
    },
    "CreateGwtGeneratorByFunctionSubGraph": {
        "handler": run_create_gwt_generator_by_function_sub_graph,
        "description": "CreateGwtGeneratorByFunctionSubGraph를 즉시 실행",
        "usage": "run runGraph SubGraph CreateGwtGeneratorByFunctionSubGraph"
    },
    "CreateUiComponentsSubGraph": {
        "handler": run_create_ui_components_subgraph,
        "description": "CreateUiComponentsSubGraph를 즉시 실행",
        "usage": "run runGraph SubGraph CreateUiComponentsSubGraph"
    },
    "ESValueSummaryGeneratorSubGraph": {
        "handler": run_es_value_summary_generator_sub_graph,
        "description": "ESValueSummaryGeneratorSubGraph를 즉시 실행",
        "usage": "run runGraph SubGraph ESValueSummaryGeneratorSubGraph"
    }
}

def run_sub_graph(command_args):
    sub_graph_name = command_args[1]

    sub_graph = run_sub_graph_registry.get(sub_graph_name, None)
    if not sub_graph:
        print(f"유효하지 않은 서브그래프 명령어입니다. {sub_graph_name}")
        return False
    return sub_graph["handler"](command_args)