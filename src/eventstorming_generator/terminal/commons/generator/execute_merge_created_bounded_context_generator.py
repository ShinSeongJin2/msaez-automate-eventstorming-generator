from ...terminal_helper import TerminalHelper
from ....generators import MergeCreatedBoundedContextGenerator
from ....models import MergeCreatedBoundedContextGeneratorOutput
from ..mocks import merge_created_bounded_context_generator_inputs

def execute_merge_created_bounded_context_generator(is_save_to_temp: bool = True) -> MergeCreatedBoundedContextGeneratorOutput:
    return TerminalHelper.run_generator(
        MergeCreatedBoundedContextGenerator, merge_created_bounded_context_generator_inputs, "normal", is_save_to_temp
    )