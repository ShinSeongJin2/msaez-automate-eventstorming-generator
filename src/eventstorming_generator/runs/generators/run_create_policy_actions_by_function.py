from ..run_util import RunUtil
from ...generators import CreatePolicyActionsByFunction
from ..mocks import create_policy_actions_by_function_inputs

def run_create_policy_actions_by_function():
    RunUtil.run_generator(CreatePolicyActionsByFunction, create_policy_actions_by_function_inputs, "normal")