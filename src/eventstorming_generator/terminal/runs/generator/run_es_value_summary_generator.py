from ...terminal_util import TerminalUtil
from ....generators import ESValueSummaryGenerator
from ..mocks import es_value_summary_generator_inputs

def run_es_value_summary_generator(command_args):
    TerminalUtil.run_generator(ESValueSummaryGenerator, es_value_summary_generator_inputs, "light")