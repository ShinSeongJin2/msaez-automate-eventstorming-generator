from ...terminal_helper import TerminalHelper
from ....generators import CreateDraftGenerator
from ....models import CreateDraftGeneratorOutput
from ..mocks import create_draft_generator_inputs

def execute_create_draft_generator(is_save_to_temp: bool = True) -> CreateDraftGeneratorOutput:
    return TerminalHelper.run_generator(
        CreateDraftGenerator, create_draft_generator_inputs, "normal", is_save_to_temp
    )