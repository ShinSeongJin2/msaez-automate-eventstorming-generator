from ...terminal_util import TerminalUtil
from ....generators import CreateAggregateClassIdByDrafts
from ..mocks import create_aggregate_class_id_by_drafts_inputs

def run_create_aggregate_class_id_by_drafts(command_args):
    TerminalUtil.run_generator(CreateAggregateClassIdByDrafts, create_aggregate_class_id_by_drafts_inputs, "light")