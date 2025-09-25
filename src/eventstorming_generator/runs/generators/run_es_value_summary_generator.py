from ..run_util import RunUtil
from ...generators import ESValueSummaryGenerator
from ..mocks import es_value_summary_generator_inputs

def run_es_value_summary_generator():
    RunUtil.run_generator(ESValueSummaryGenerator, es_value_summary_generator_inputs, "light")