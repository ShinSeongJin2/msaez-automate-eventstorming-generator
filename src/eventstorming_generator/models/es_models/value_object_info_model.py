from typing import Optional
from pydantic import Field

from ..base import BaseModelWithItem
from .referenced_aggregate_info_model import ReferencedAggregateInfoModel

class ValueObjectInfoModel(BaseModelWithItem):
    """Value Object Information"""
    name: str = Field(..., description="Value Object name (English PascalCase)")
    alias: str = Field(..., description="Value Object alias (preferred language)")
    referencedAggregate: Optional[ReferencedAggregateInfoModel] = None