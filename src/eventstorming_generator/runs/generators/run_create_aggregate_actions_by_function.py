from ..run_util import RunUtil
from ...generators import CreateAggregateActionsByFunction
from ..mocks import create_aggregate_actions_by_function_inputs

def run_create_aggregate_actions_by_function():
    RunUtil.run_generator(CreateAggregateActionsByFunction, create_aggregate_actions_by_function_inputs, "normal")