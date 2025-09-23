from ..test_utils import TestUtils
from ...generators import CreateCommandActionsByFunction
from ..mocks import create_command_actions_by_function_inputs

def test_create_command_actions_by_function():
    TestUtils.test_generator(CreateCommandActionsByFunction, create_command_actions_by_function_inputs, "light")