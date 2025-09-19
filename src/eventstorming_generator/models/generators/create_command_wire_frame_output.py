from pydantic import Field
from ..base import BaseModelWithItem

class WireFrameResult(BaseModelWithItem):
    """Contains the generated HTML wireframe"""
    html: str = Field(description="Complete HTML wireframe code starting with any custom <style> tag you need, followed by <div> container, using embedded CSS for reused styles and inline CSS for unique styles (NO JavaScript). Do not include the common styles block.")

class CreateCommandWireFrameOutput(BaseModelWithItem):
    """Output model for creating command wireframe with structured reasoning and HTML result"""
    inference: str = Field(description="Detailed reasoning about wireframe design decisions")
    result: WireFrameResult = Field(description="The generated HTML wireframe result")