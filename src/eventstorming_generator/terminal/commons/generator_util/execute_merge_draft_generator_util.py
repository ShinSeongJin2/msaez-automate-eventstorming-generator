from typing import List

from ....generators import MergeDraftGeneratorUtil
from ....models import BoundedContextStructureModel
from ..mocks import merge_draft_generator_util_inputs
from ....config import Config

def execute_sequential_merge_drafts_safely() -> List[BoundedContextStructureModel]:
    return MergeDraftGeneratorUtil.sequential_merge_drafts_safely(
        merge_draft_generator_util_inputs,
        Config.get_ai_model(),
        "Korean",
        5,
        3,
        "temp_job_id"
    )