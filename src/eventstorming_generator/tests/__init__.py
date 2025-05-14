from .test_graph import test_graph
from .test_es_actions import test_es_value_creation
from .test_create_bounded_contexts import test_create_bounded_contexts
from .test_fake_actions_util import test_fake_actions_util
from .generators import test_create_aggregate_actions_by_function, test_sanity_check_generator, test_create_aggregate_class_id_by_drafts
from .subgraphs import test_create_aggregate_by_functions_sub_graph, test_create_aggregate_class_id_by_drafts_sub_graph

test_commands = {
    "test_graph": test_graph,
    "test_es_value_creation": test_es_value_creation,
    "test_create_bounded_contexts": test_create_bounded_contexts,
    "test_fake_actions_util": test_fake_actions_util,
    "test_sanity_check_generator": test_sanity_check_generator,
    "test_create_aggregate_actions_by_function": test_create_aggregate_actions_by_function,
    "test_create_aggregate_by_functions_sub_graph": test_create_aggregate_by_functions_sub_graph,
    "test_create_aggregate_class_id_by_drafts": test_create_aggregate_class_id_by_drafts,
    "test_create_aggregate_class_id_by_drafts_sub_graph": test_create_aggregate_class_id_by_drafts_sub_graph
}

__all__ = [
    "test_commands"
]
