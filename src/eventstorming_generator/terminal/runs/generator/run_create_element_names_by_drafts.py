from ...terminal_helper import TerminalHelper
from ....generators import CreateElementNamesByDrafts
from ..mocks import create_element_names_by_drafts_inputs

def run_create_element_names_by_drafts(command_args):
    TerminalHelper.run_generator(CreateElementNamesByDrafts, create_element_names_by_drafts_inputs, "normal")