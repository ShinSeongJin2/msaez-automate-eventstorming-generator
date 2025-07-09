import os

from ..test_utils import TestUtils
from ...generators import AssignFieldsToActionsGenerator
from ..mocks import assign_fields_to_actions_generator_inputs
from ...utils import LoggingUtil

def test_assign_fields_to_actions_generator():
    try:

        result = AssignFieldsToActionsGenerator(os.getenv("AI_MODEL"), {}, {
            "preferredLanguage": "Korean",
            "inputs": {
                "description": assign_fields_to_actions_generator_inputs["description"],
                "existingActions": assign_fields_to_actions_generator_inputs["existingActions"],
                "missingFields": assign_fields_to_actions_generator_inputs["missingFields"]
            }
        }).generate()
        TestUtils.save_dict_to_temp_file(result, "test_assign_fields_to_actions_generator")

    except Exception as e:
        LoggingUtil.exception("test_assign_fields_to_actions_generator", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_assign_fields_to_actions_generator_error")
        raise
