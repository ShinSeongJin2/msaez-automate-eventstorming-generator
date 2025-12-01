from ...terminal_helper import TerminalHelper
from ....generators import CreateAggregateClassIdByDrafts
from ..mocks import create_aggregate_class_id_by_drafts_inputs

def run_create_aggregate_class_id_by_drafts(command_args):
    TerminalHelper.run_generator(CreateAggregateClassIdByDrafts, create_aggregate_class_id_by_drafts_inputs, "light")