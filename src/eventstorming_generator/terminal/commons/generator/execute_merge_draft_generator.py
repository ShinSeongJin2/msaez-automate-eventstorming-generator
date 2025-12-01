from ...terminal_helper import TerminalHelper
from ....generators import MergeDraftGenerator
from ....models import MergeDraftGeneratorOutput
from ..mocks import merge_draft_generator_inputs

def execute_merge_draft_generator(is_save_to_temp: bool = True) -> MergeDraftGeneratorOutput:
    return TerminalHelper.run_generator(
        MergeDraftGenerator, merge_draft_generator_inputs, "normal", is_save_to_temp
    )