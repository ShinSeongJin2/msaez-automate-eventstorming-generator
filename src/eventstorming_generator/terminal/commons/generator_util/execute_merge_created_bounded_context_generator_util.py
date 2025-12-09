from typing import List

from ....generators import MergeCreatedBoundedContextGeneratorUtil
from ....models import BoundedContextInfoModel
from ..mocks import merge_created_bounded_context_generator_util_inputs
from ....config import Config

def execute_merge_created_bounded_context_safely() -> List[BoundedContextInfoModel]:
    return MergeCreatedBoundedContextGeneratorUtil.merge_created_bounded_context_safely(
        merge_created_bounded_context_generator_util_inputs["boundedContextInfos"],
        Config.get_ai_model(),
        "Korean",
        3,
        "temp_job_id"
    )