import os

from ..test_utils import TestUtils
from ...generators import CreatePolicyActionsByFunction
from ..mocks import create_policy_actions_by_function_inputs
from ...utils import LoggingUtil

def test_create_policy_actions_by_function():
    try:

        result = CreatePolicyActionsByFunction(os.getenv("AI_MODEL"), {}, {
            "preferredLanguage": "Korean",
            "inputs": {
                "summarizedESValue": create_policy_actions_by_function_inputs["summarizedESValue"],
                "description": create_policy_actions_by_function_inputs["description"]
            }
        }).generate()
        TestUtils.save_dict_to_temp_file(result, "test_create_policy_actions_by_function")

    except Exception as e:
        LoggingUtil.exception("test_create_policy_actions_by_function", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_create_policy_actions_by_function_error")
        raise
