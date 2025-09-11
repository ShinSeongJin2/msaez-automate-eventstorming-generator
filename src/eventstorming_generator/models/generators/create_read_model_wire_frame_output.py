from pydantic import Field
from ..base import BaseModelWithItem

class WireFrameResult(BaseModelWithItem):
    """Contains the generated HTML wireframe"""
    html: str = Field(description="HTML wireframe code for the read model view")

class CreateReadModelWireFrameOutput(BaseModelWithItem):
    """Output model for creating read model wireframes with structured reasoning and HTML results"""
    inference: str = Field(description="Detailed reasoning and analysis for the generated wireframe")
    result: WireFrameResult = Field(description="The generated HTML wireframe result")