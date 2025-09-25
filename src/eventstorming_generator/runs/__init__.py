from .run_graph import run_graph
from .run_create_bounded_contexts_graph import run_create_bounded_contexts_graph
from .subgraphs import run_create_aggregate_by_functions_sub_graph, run_create_aggregate_class_id_by_drafts_sub_graph, run_create_element_names_by_draft_sub_graph, run_create_command_actions_by_function_sub_graph, run_create_policy_actions_by_function_sub_graph, run_create_gwt_generator_by_function_sub_graph, run_create_ui_components_subgraph, run_es_value_summary_generator_sub_graph, run_aggregate_worker_subgraph, run_class_id_worker_subgraph, run_command_actions_worker_subgraph, run_policy_actions_worker_subgraph, run_gwt_worker_sub_graph, run_ui_component_worker_subgraph

from .generators import run_create_aggregate_actions_by_function, run_create_aggregate_class_id_by_drafts, run_assign_fields_to_actions_generator, run_create_element_names_by_drafts, run_create_command_actions_by_function, run_create_policy_actions_by_function, run_create_gwt_generator_by_function, run_create_command_wire_frame, run_create_read_model_wire_frame,  run_es_value_summary_generator

from .utils import run_es_value_creation_with_actions_collection, run_es_value_creation_with_total_actions, run_es_value_creation_with_mocked_actions, run_fake_actions_util, run_token_counter, run_xml_util

from ..types import RunableLogicsCategories

runable_logics_categories: RunableLogicsCategories = {
    "run_main_graphs": {
        "run_graph": run_graph,
        "run_create_bounded_contexts_graph": run_create_bounded_contexts_graph,
        "run_create_aggregate_by_functions_sub_graph": run_create_aggregate_by_functions_sub_graph,
        "run_create_aggregate_class_id_by_drafts_sub_graph": run_create_aggregate_class_id_by_drafts_sub_graph,
        "run_create_element_names_by_draft_sub_graph": run_create_element_names_by_draft_sub_graph,
        "run_create_command_actions_by_function_sub_graph": run_create_command_actions_by_function_sub_graph,
        "run_create_policy_actions_by_function_sub_graph": run_create_policy_actions_by_function_sub_graph,
        "run_create_gwt_generator_by_function_sub_graph": run_create_gwt_generator_by_function_sub_graph,
        "run_create_ui_components_subgraph": run_create_ui_components_subgraph,
        "run_es_value_summary_generator_sub_graph": run_es_value_summary_generator_sub_graph
    },
    "run_worker_subgraphs": {
        "run_aggregate_worker_subgraph": run_aggregate_worker_subgraph,
        "run_class_id_worker_subgraph": run_class_id_worker_subgraph,
        "run_command_actions_worker_subgraph": run_command_actions_worker_subgraph,
        "run_policy_actions_worker_subgraph": run_policy_actions_worker_subgraph,
        "run_gwt_worker_sub_graph": run_gwt_worker_sub_graph,
        "run_ui_component_worker_subgraph": run_ui_component_worker_subgraph,
    },
    "run_generators": {
        "run_create_aggregate_actions_by_function": run_create_aggregate_actions_by_function,
        "run_assign_fields_to_actions_generator": run_assign_fields_to_actions_generator,
        "run_create_aggregate_class_id_by_drafts": run_create_aggregate_class_id_by_drafts,
        "run_create_element_names_by_drafts": run_create_element_names_by_drafts,
        "run_create_command_actions_by_function": run_create_command_actions_by_function,
        "run_create_policy_actions_by_function": run_create_policy_actions_by_function,
        "run_create_gwt_generator_by_function": run_create_gwt_generator_by_function,
        "run_create_command_wire_frame": run_create_command_wire_frame,
        "run_create_read_model_wire_frame": run_create_read_model_wire_frame,
        "run_es_value_summary_generator": run_es_value_summary_generator
    },
    "run_utils": {
        "run_es_value_creation_with_actions_collection": run_es_value_creation_with_actions_collection,
        "run_es_value_creation_with_total_actions": run_es_value_creation_with_total_actions,
        "run_es_value_creation_with_mocked_actions": run_es_value_creation_with_mocked_actions,
        "run_fake_actions_util": run_fake_actions_util,
        "run_token_counter": run_token_counter,
        "run_xml_util": run_xml_util
    }
}

__all__ = [
    "runable_logics_categories"
]
