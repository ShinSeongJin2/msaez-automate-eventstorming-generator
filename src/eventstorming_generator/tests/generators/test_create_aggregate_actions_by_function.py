import os

from ..test_utils import TestUtils
from ...generators import CreateAggregateActionsByFunction
from ..mocks import create_aggregate_actions_by_function_inputs
from ...utils import LoggingUtil

def test_create_aggregate_actions_by_function():
    try:

        generator = CreateAggregateActionsByFunction(os.getenv("AI_MODEL"), {}, {
            "preferredLanguage": "Korean",
            "inputs": {
                "summarizedESValue": create_aggregate_actions_by_function_inputs["summarizedESValue"],
                "targetBoundedContext": create_aggregate_actions_by_function_inputs["targetBoundedContext"],
                "description": create_aggregate_actions_by_function_inputs["description"],
                "draftOption": create_aggregate_actions_by_function_inputs["draftOption"],
                "targetAggregate": create_aggregate_actions_by_function_inputs["targetAggregate"]
            }
        })
        result = generator.generate()
        TestUtils.save_dict_to_temp_file(result, "test_create_aggregate_actions_by_function")

    except Exception as e:
        LoggingUtil.exception("test_create_aggregate_actions_by_function", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_create_aggregate_actions_by_function_error")
        raise
