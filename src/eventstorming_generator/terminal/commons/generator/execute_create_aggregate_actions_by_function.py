from ...terminal_helper import TerminalHelper
from ....generators import CreateAggregateActionsByFunction
from ....models import CreateAggregateActionsByFunctionOutput
from ..mocks import create_aggregate_actions_by_function_inputs

def execute_create_aggregate_actions_by_function(is_save_to_temp: bool = True) -> CreateAggregateActionsByFunctionOutput:
    return TerminalHelper.run_generator(
        CreateAggregateActionsByFunction, create_aggregate_actions_by_function_inputs, "normal", is_save_to_temp
    )