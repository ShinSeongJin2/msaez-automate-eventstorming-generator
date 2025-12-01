from ...terminal_helper import TerminalHelper
from ....generators import AssignFieldsToActionsGenerator
from ....models import AssignFieldsToActionsGeneratorOutput
from ..mocks import assign_fields_to_actions_generator_inputs

def execute_assign_fields_to_actions_generator(is_save_to_temp: bool = True) -> AssignFieldsToActionsGeneratorOutput:
    return TerminalHelper.run_generator(
        AssignFieldsToActionsGenerator, assign_fields_to_actions_generator_inputs, "normal", is_save_to_temp
    )