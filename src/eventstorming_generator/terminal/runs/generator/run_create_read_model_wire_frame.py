from ...terminal_helper import TerminalHelper
from ....generators import CreateReadModelWireFrame
from ..mocks import create_read_model_wire_frame_inputs

def run_create_read_model_wire_frame(command_args):
    TerminalHelper.run_generator(CreateReadModelWireFrame, create_read_model_wire_frame_inputs, "light")