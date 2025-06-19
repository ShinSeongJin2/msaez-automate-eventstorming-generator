import os

from ..test_utils import TestUtils
from ...generators import CreateCommandActionsByFunction
from ..mocks import create_command_actions_by_function_inputs
from ...utils import LoggingUtil

def test_create_command_actions_by_function():
    try:

        result = CreateCommandActionsByFunction(os.getenv("AI_MODEL"), {}, {
            "preferredLanguage": "Korean",
            "inputs": {
                "summarizedESValue": create_command_actions_by_function_inputs["summarizedESValue"],
                "description": create_command_actions_by_function_inputs["description"],
                "targetAggregate": create_command_actions_by_function_inputs["targetAggregate"]
            }
        }).generate()
        TestUtils.save_dict_to_temp_file(result, "test_create_command_actions_by_function")

    except Exception as e:
        LoggingUtil.exception("test_create_command_actions_by_function", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_create_command_actions_by_function_error")
        raise
