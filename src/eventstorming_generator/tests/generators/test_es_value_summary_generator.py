from ..test_utils import TestUtils
from ...generators import ESValueSummaryGenerator
from ..mocks import es_value_summary_generator_inputs

def test_es_value_summary_generator():
    TestUtils.test_generator(ESValueSummaryGenerator, es_value_summary_generator_inputs, "light")