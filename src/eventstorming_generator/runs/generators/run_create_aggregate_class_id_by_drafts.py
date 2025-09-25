from ..run_util import RunUtil
from ...generators import CreateAggregateClassIdByDrafts
from ..mocks import create_aggregate_class_id_by_drafts_inputs

def run_create_aggregate_class_id_by_drafts():
    RunUtil.run_generator(CreateAggregateClassIdByDrafts, create_aggregate_class_id_by_drafts_inputs, "light")