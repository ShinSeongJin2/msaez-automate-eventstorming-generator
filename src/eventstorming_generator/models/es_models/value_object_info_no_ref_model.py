from pydantic import Field

from ..base import BaseModelWithItem

class ValueObjectInfoNoRefModel(BaseModelWithItem):
    """Value Object No Ref Information"""
    name: str = Field(..., description="Value Object name (English PascalCase)")
    alias: str = Field(..., description="Value Object alias (preferred language)")