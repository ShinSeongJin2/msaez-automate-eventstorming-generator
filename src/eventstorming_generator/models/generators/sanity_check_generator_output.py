from pydantic import Field
from ..base import BaseModelWithItem

class SanityCheckGeneratorOutput(BaseModelWithItem):
    """Structured Output Model of the SanityCheck Generator"""
    output: str = Field(description="Text entered by the user")