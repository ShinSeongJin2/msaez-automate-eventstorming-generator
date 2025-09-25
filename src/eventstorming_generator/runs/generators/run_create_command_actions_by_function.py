from ..run_util import RunUtil
from ...generators import CreateCommandActionsByFunction
from ..mocks import create_command_actions_by_function_inputs

def run_create_command_actions_by_function():
    RunUtil.run_generator(CreateCommandActionsByFunction, create_command_actions_by_function_inputs, "light")