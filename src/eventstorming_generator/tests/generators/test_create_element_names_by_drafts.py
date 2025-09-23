from ..test_utils import TestUtils
from ...generators import CreateElementNamesByDrafts
from ..mocks import create_element_names_by_drafts_inputs

def test_create_element_names_by_drafts():
    TestUtils.test_generator(CreateElementNamesByDrafts, create_element_names_by_drafts_inputs, "light")