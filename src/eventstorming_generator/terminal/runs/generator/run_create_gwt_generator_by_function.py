from ...terminal_helper import TerminalHelper
from ....generators import CreateGWTGeneratorByFunction
from ..mocks import create_gwt_generator_by_function_inputs

def run_create_gwt_generator_by_function(command_args):
    TerminalHelper.run_generator(CreateGWTGeneratorByFunction, create_gwt_generator_by_function_inputs, "light")