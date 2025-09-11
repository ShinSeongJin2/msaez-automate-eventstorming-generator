import os

from ..test_utils import TestUtils
from ...generators import CreateCommandWireFrame
from ..mocks import create_command_wire_frame_inputs
from ...utils import LoggingUtil

def test_create_command_wire_frame():
    try:

        generator = CreateCommandWireFrame(os.getenv("AI_MODEL"), {}, {
            "preferredLanguage": "Korean",
            "inputs": {
                "commandName": create_command_wire_frame_inputs["commandName"],
                "commandDisplayName": create_command_wire_frame_inputs["commandDisplayName"],
                "fields": create_command_wire_frame_inputs["fields"],
                "api": create_command_wire_frame_inputs["api"],
                "additionalRequirements": create_command_wire_frame_inputs["additionalRequirements"]
            }
        })
        result = generator.generate()
        TestUtils.save_dict_to_temp_file(result, "test_create_command_wire_frame")

    except Exception as e:
        LoggingUtil.exception("test_create_command_wire_frame", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_create_command_wire_frame")
        raise
