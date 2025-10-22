from ...terminal_util import TerminalUtil
from ....generators import CreateReadModelWireFrame
from ..mocks import create_read_model_wire_frame_inputs

def run_create_read_model_wire_frame(command_args):
    TerminalUtil.run_generator(CreateReadModelWireFrame, create_read_model_wire_frame_inputs, "light")