from ..run_util import RunUtil
from ...generators import CreateCommandWireFrame
from ..mocks import create_command_wire_frame_inputs

def run_create_command_wire_frame():
    RunUtil.run_generator(CreateCommandWireFrame, create_command_wire_frame_inputs, "light")