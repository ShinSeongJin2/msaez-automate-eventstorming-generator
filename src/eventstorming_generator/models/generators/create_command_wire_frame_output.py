from pydantic import Field
from ..base import BaseModelWithItem

class WireFrameResult(BaseModelWithItem):
    """Contains the generated HTML wireframe"""
    html: str = Field(description="Generated HTML wireframe code for the command interface")

class CreateCommandWireFrameOutput(BaseModelWithItem):
    """Output model for creating command wireframe with structured reasoning and HTML result"""
    inference: str = Field(description="Detailed reasoning and analysis for the generated wireframe")
    result: WireFrameResult = Field(description="The generated HTML wireframe result")