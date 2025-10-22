from ...terminal_util import TerminalUtil
from ....generators import AssignFieldsToActionsGenerator
from ..mocks import assign_fields_to_actions_generator_inputs

def run_assign_fields_to_actions_generator(command_args):
    TerminalUtil.run_generator(AssignFieldsToActionsGenerator, assign_fields_to_actions_generator_inputs, "normal")