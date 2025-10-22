from ...terminal_util import TerminalUtil
from ....generators import CreateElementNamesByDrafts
from ..mocks import create_element_names_by_drafts_inputs

def run_create_element_names_by_drafts(command_args):
    TerminalUtil.run_generator(CreateElementNamesByDrafts, create_element_names_by_drafts_inputs, "normal")