from .test_es_actions import test_es_value_creation
from .test_create_bounded_contexts import test_create_bounded_contexts
from .test_fake_actions_util import test_fake_actions_util
from .test_sanity_check_generator import test_sanity_check_generator

test_commands = {
    "test_es_value_creation": test_es_value_creation,
    "test_create_bounded_contexts": test_create_bounded_contexts,
    "test_fake_actions_util": test_fake_actions_util,
    "test_sanity_check_generator": test_sanity_check_generator
}

__all__ = [
    "test_commands"
]
