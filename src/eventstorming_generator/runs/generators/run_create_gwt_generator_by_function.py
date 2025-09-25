from ..run_util import RunUtil
from ...generators import CreateGWTGeneratorByFunction
from ..mocks import create_gwt_generator_by_function_inputs

def run_create_gwt_generator_by_function():
    RunUtil.run_generator(CreateGWTGeneratorByFunction, create_gwt_generator_by_function_inputs, "light")