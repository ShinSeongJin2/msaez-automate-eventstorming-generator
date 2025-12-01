from ...terminal_helper import TerminalHelper
from ....generators import CreateCommandWireFrame
from ..mocks import create_command_wire_frame_inputs

def run_create_command_wire_frame(command_args):
    TerminalHelper.run_generator(CreateCommandWireFrame, create_command_wire_frame_inputs, "light")