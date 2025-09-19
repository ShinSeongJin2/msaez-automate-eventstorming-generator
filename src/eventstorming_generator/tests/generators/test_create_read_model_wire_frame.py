from ..test_utils import TestUtils
from ...generators import CreateReadModelWireFrame
from ..mocks import create_read_model_wire_frame_inputs

def test_create_read_model_wire_frame():
    TestUtils.test_generator(CreateReadModelWireFrame, create_read_model_wire_frame_inputs, "light")