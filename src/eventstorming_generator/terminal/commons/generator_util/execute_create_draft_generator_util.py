from ....generators import CreateDraftGeneratorUtil
from ....models import BoundedContextStructureModel
from ..mocks import create_draft_generator_util_inputs
from ....config import Config

def execute_create_draft_by_function_safely() -> BoundedContextStructureModel:
    return CreateDraftGeneratorUtil.create_draft_by_function_safely(
        create_draft_generator_util_inputs["boundedContext"],
        create_draft_generator_util_inputs["requirements"],
        Config.get_ai_model(),
        "Korean",
        3,
        "temp_job_id"
    )