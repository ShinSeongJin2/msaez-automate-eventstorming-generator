from ...terminal_helper import TerminalHelper
from ....generators import CreateCommandActionsByFunction
from ..mocks import create_command_actions_by_function_inputs

def run_create_command_actions_by_function(command_args):
    TerminalHelper.run_generator(CreateCommandActionsByFunction, create_command_actions_by_function_inputs, "light")