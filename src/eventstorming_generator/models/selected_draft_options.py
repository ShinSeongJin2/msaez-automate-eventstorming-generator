from pydantic import BaseModel, Field
from typing import Optional, List
from .eventstorming import BoundedContextModel

class ReferencedAggregateInfo(BaseModel):
    name: Optional[str] = None
    alias: Optional[str] = None

class ValueObjectInfo(BaseModel):
    name: Optional[str] = None
    alias: Optional[str] = None
    referencedAggregate: Optional[ReferencedAggregateInfo] = None

class EnumerationInfo(BaseModel):
    name: Optional[str] = None
    alias: Optional[str] = None

class AggregateInfo(BaseModel):
    name: Optional[str] = None
    alias: Optional[str] = None

class StructureItem(BaseModel):
    aggregate: Optional[AggregateInfo] = None
    enumerations: Optional[List[EnumerationInfo]] = Field(default_factory=list)
    valueObjects: Optional[List[ValueObjectInfo]] = Field(default_factory=list)

class ProsConsModel(BaseModel):
    cohesion: Optional[str] = None
    coupling: Optional[str] = None
    consistency: Optional[str] = None
    encapsulation: Optional[str] = None
    complexity: Optional[str] = None
    independence: Optional[str] = None
    performance: Optional[str] = None

class SelectedDraftOptionItem(BaseModel):
    structure: Optional[List[StructureItem]] = Field(default_factory=list)
    pros: Optional[ProsConsModel] = None
    cons: Optional[ProsConsModel] = None
    isAIRecommended: Optional[bool] = None
    boundedContext: Optional[BoundedContextModel] = None
    description: Optional[str] = None