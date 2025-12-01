from typing import Literal
from pydantic import Field

from ..base import BaseModelWithItem

class BoundedContextInfoModel(BaseModelWithItem):
    """Bounded Context model"""
    name: str = Field(..., description="Bounded Context name (English PascalCase)")
    alias: str = Field(..., description="Bounded Context alias (preferred language)")
    importance: Literal["Core Domain", "Supporting Domain", "Generic Domain"] = Field(..., description="Domain importance")
    description: str = Field(..., description="Bounded Context description")