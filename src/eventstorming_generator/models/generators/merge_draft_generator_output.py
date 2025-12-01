from typing import List
from pydantic import Field

from ..base import BaseModelWithItem
from ..es_models import EnumerationInfoModel, ValueObjectInfoNoRefModel

class IDValueObjectInfo(BaseModelWithItem):
    """ID Value Object Information for referencing other aggregates"""
    name: str = Field(..., description="ID Value Object name (English PascalCase)")
    alias: str = Field(..., description="ID Value Object alias (preferred language)")
    referencedAggregateName: str = Field(..., description="Referenced aggregate name")
    referencedAggregateAlias: str = Field(..., description="Referenced aggregate alias")

class MergedAggregateInfo(BaseModelWithItem):
    """Merged Aggregate Information"""
    aggregateName: str = Field(..., description="Aggregate name (English PascalCase)")
    aggregateAlias: str = Field(..., description="Aggregate alias (preferred language)")
    enumerations: List[EnumerationInfoModel] = Field(default_factory=list, description="List of enumerations")
    valueObjects: List[ValueObjectInfoNoRefModel] = Field(default_factory=list, description="List of value objects")
    IDValueObjects: List[IDValueObjectInfo] = Field(default_factory=list, description="List of ID value objects for referencing other aggregates")

class MergedDraftInfo(BaseModelWithItem):
    """Merged Draft Information per Bounded Context"""
    boundedContextName: str = Field(..., description="Bounded context name")
    aggregates: List[MergedAggregateInfo] = Field(..., description="List of merged aggregates")

class MergeDraftGeneratorOutput(BaseModelWithItem):
    """Merge Draft Generator Output"""
    mergedDrafts: List[MergedDraftInfo] = Field(..., description="List of merged drafts for target bounded contexts")