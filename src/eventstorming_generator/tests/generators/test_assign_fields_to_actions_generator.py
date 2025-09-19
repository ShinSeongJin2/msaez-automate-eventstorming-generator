from ..test_utils import TestUtils
from ...generators import AssignFieldsToActionsGenerator
from ..mocks import assign_fields_to_actions_generator_inputs

def test_assign_fields_to_actions_generator():
    TestUtils.test_generator(AssignFieldsToActionsGenerator, assign_fields_to_actions_generator_inputs, "light")