from ..run_util import RunUtil
from ...generators import CreateElementNamesByDrafts
from ..mocks import create_element_names_by_drafts_inputs

def run_create_element_names_by_drafts():
    RunUtil.run_generator(CreateElementNamesByDrafts, create_element_names_by_drafts_inputs, "normal")