from .test_graph import test_graph
from .test_create_bounded_contexts import test_create_bounded_contexts
from .utils import test_es_value_creation, test_fake_actions_util, test_token_counter
from .generators import test_create_aggregate_actions_by_function, test_sanity_check_generator, test_create_aggregate_class_id_by_drafts, test_create_command_actions_by_function, test_create_gwt_generator_by_function, test_create_policy_actions_by_function, test_es_value_summary_generator, test_extract_ddl_fields_generator, test_assign_fields_to_actions_generator, test_assign_ddl_fields_to_aggregate_draft, test_assign_event_names_to_aggregate_draft
from .subgraphs import test_create_aggregate_by_functions_sub_graph, test_create_aggregate_class_id_by_drafts_sub_graph, test_create_command_actions_by_function_sub_graph, test_create_policy_actions_by_function_sub_graph, test_create_gwt_generator_by_function_sub_graph, test_es_value_summary_generator_sub_graph

test_commands = {
    "test_graph": test_graph,
    "test_es_value_creation": test_es_value_creation,
    "test_create_bounded_contexts": test_create_bounded_contexts,
    "test_fake_actions_util": test_fake_actions_util,
    "test_sanity_check_generator": test_sanity_check_generator,
    "test_create_aggregate_actions_by_function": test_create_aggregate_actions_by_function,
    "test_create_aggregate_by_functions_sub_graph": test_create_aggregate_by_functions_sub_graph,
    "test_create_aggregate_class_id_by_drafts": test_create_aggregate_class_id_by_drafts,
    "test_create_aggregate_class_id_by_drafts_sub_graph": test_create_aggregate_class_id_by_drafts_sub_graph,
    "test_create_command_actions_by_function": test_create_command_actions_by_function,
    "test_create_command_actions_by_function_sub_graph": test_create_command_actions_by_function_sub_graph,
    "test_create_policy_actions_by_function": test_create_policy_actions_by_function,
    "test_create_policy_actions_by_function_sub_graph": test_create_policy_actions_by_function_sub_graph,
    "test_create_gwt_generator_by_function": test_create_gwt_generator_by_function,
    "test_create_gwt_generator_by_function_sub_graph": test_create_gwt_generator_by_function_sub_graph,
    "test_es_value_summary_generator": test_es_value_summary_generator,
    "test_es_value_summary_generator_sub_graph": test_es_value_summary_generator_sub_graph,
    "test_token_counter": test_token_counter,
    "test_extract_ddl_fields_generator": test_extract_ddl_fields_generator,
    "test_assign_fields_to_actions_generator": test_assign_fields_to_actions_generator,
    "test_assign_ddl_fields_to_aggregate_draft": test_assign_ddl_fields_to_aggregate_draft,
    "test_assign_event_names_to_aggregate_draft": test_assign_event_names_to_aggregate_draft
}

__all__ = [
    "test_commands"
]
