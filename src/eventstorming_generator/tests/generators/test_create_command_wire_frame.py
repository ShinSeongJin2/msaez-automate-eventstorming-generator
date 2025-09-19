from ..test_utils import TestUtils
from ...generators import CreateCommandWireFrame
from ..mocks import create_command_wire_frame_inputs

def test_create_command_wire_frame():
    TestUtils.test_generator(CreateCommandWireFrame, create_command_wire_frame_inputs, "light")