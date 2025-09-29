from pydantic import Field
from ..base import BaseModelWithItem

class CreateReadModelWireFrameOutput(BaseModelWithItem):
    """Output model for creating read model wireframes"""
    html: str = Field(description="Complete HTML wireframe code starting with any custom <style> tag you need, followed by <div> container, using embedded CSS for reused styles and inline CSS for unique styles (NO JavaScript). Do not include the common styles block.")