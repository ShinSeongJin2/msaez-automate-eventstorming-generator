from ...terminal_helper import TerminalHelper
from ....generators import CreateBoundedContextGenerator
from ....models import CreateBoundedContextGeneratorOutput
from ..mocks import create_bounded_context_generator_inputs

def execute_create_bounded_context_generator(is_save_to_temp: bool = True) -> CreateBoundedContextGeneratorOutput:
    return TerminalHelper.run_generator(
        CreateBoundedContextGenerator, create_bounded_context_generator_inputs, "normal", is_save_to_temp
    )