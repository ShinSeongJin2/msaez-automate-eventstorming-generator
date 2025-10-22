from ...terminal_util import TerminalUtil
from ....generators import CreatePolicyActionsByFunction
from ..mocks import create_policy_actions_by_function_inputs

def run_create_policy_actions_by_function(command_args):
    TerminalUtil.run_generator(CreatePolicyActionsByFunction, create_policy_actions_by_function_inputs, "normal")