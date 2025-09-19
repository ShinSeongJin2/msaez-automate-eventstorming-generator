from ..test_utils import TestUtils
from ...generators import CreateAggregateActionsByFunction
from ..mocks import create_aggregate_actions_by_function_inputs

def test_create_aggregate_actions_by_function():
    TestUtils.test_generator(CreateAggregateActionsByFunction, create_aggregate_actions_by_function_inputs, "light")