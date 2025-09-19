from ..test_utils import TestUtils
from ...generators import CreateGWTGeneratorByFunction
from ..mocks import create_gwt_generator_by_function_inputs

def test_create_gwt_generator_by_function():
    TestUtils.test_generator(CreateGWTGeneratorByFunction, create_gwt_generator_by_function_inputs, "light")