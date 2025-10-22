from ...terminal_util import TerminalUtil
from ....generators import CreateAggregateActionsByFunction
from ..mocks import create_aggregate_actions_by_function_inputs

def run_create_aggregate_actions_by_function(command_args):
    TerminalUtil.run_generator(CreateAggregateActionsByFunction, create_aggregate_actions_by_function_inputs, "normal")