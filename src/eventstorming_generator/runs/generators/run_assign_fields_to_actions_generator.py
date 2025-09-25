from ..run_util import RunUtil
from ...generators import AssignFieldsToActionsGenerator
from ..mocks import assign_fields_to_actions_generator_inputs

def run_assign_fields_to_actions_generator():
    RunUtil.run_generator(AssignFieldsToActionsGenerator, assign_fields_to_actions_generator_inputs, "normal")