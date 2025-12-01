from typing import List
from pydantic import Field

from ..base import BaseModelWithItem

class EnumerationInfoModel(BaseModelWithItem):
    """Enumeration Information"""
    name: str = Field(..., description="Enumeration name (English PascalCase)")
    alias: str = Field(..., description="Enumeration alias (preferred language)")