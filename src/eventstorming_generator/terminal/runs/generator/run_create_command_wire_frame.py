from ...terminal_util import TerminalUtil
from ....generators import CreateCommandWireFrame
from ..mocks import create_command_wire_frame_inputs

def run_create_command_wire_frame(command_args):
    TerminalUtil.run_generator(CreateCommandWireFrame, create_command_wire_frame_inputs, "light")