import os

from ..test_utils import TestUtils
from ...generators import CreateReadModelWireFrame
from ..mocks import create_read_model_wire_frame_inputs
from ...utils import LoggingUtil

def test_create_read_model_wire_frame():
    try:

        generator = CreateReadModelWireFrame(os.getenv("AI_MODEL"), {}, {
            "preferredLanguage": "Korean",
            "inputs": {
                "viewName": create_read_model_wire_frame_inputs["viewName"],
                "viewDisplayName": create_read_model_wire_frame_inputs["viewDisplayName"],
                "aggregateFields": create_read_model_wire_frame_inputs["aggregateFields"],
                "viewQueryParameters": create_read_model_wire_frame_inputs["viewQueryParameters"],
                "additionalRequirements": create_read_model_wire_frame_inputs["additionalRequirements"]
            }
        })
        result = generator.generate()
        TestUtils.save_dict_to_temp_file(result, "test_create_read_model_wire_frame")

    except Exception as e:
        LoggingUtil.exception("test_create_read_model_wire_frame", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_create_read_model_wire_frame_error")
        raise
