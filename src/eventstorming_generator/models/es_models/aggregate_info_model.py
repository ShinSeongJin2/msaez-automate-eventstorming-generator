from typing import List
from pydantic import Field

from ..base import BaseModelWithItem
from .enumeration_info_model import EnumerationInfoModel
from .value_object_info_model import ValueObjectInfoModel

class AggregateInfoModel(BaseModelWithItem):
    """Aggregate Information"""
    aggregateName: str = Field(..., description="Aggregate name (English PascalCase)")
    aggregateAlias: str = Field(..., description="Aggregate alias (preferred language)")
    enumerations: List[EnumerationInfoModel] = Field(default_factory=list, description="List of enumerations")
    valueObjects: List[ValueObjectInfoModel] = Field(default_factory=list, description="List of value objects")