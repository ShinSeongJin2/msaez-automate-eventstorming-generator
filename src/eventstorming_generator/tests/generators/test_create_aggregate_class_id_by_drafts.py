from ..test_utils import TestUtils
from ...generators import CreateAggregateClassIdByDrafts
from ..mocks import create_aggregate_class_id_by_drafts_inputs

def test_create_aggregate_class_id_by_drafts():
    TestUtils.test_generator(CreateAggregateClassIdByDrafts, create_aggregate_class_id_by_drafts_inputs, "light")