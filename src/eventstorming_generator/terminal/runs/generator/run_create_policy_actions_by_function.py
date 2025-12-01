from ...terminal_helper import TerminalHelper
from ....generators import CreatePolicyActionsByFunction
from ..mocks import create_policy_actions_by_function_inputs

def run_create_policy_actions_by_function(command_args):
    TerminalHelper.run_generator(CreatePolicyActionsByFunction, create_policy_actions_by_function_inputs, "normal")