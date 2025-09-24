from ..test_utils import TestUtils
from ...generators import CreatePolicyActionsByFunction
from ..mocks import create_policy_actions_by_function_inputs

def test_create_policy_actions_by_function():
    TestUtils.test_generator(CreatePolicyActionsByFunction, create_policy_actions_by_function_inputs, "normal")