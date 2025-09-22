from typing import List, Optional
from pydantic import Field
from ..base import BaseModelWithItem

class PropertyOutput(BaseModelWithItem):
    """Property definition for value object"""
    name: str = Field(..., description="Name of the property")
    type: Optional[str] = Field(None, description="Type of the property (optional, defaults to String)")
    isKey: Optional[bool] = Field(None, description="Whether this property is a primary key")

class ActionIds(BaseModelWithItem):
    """Identifiers for the action target"""
    boundedContextId: str = Field(..., description="ID of the bounded context")
    aggregateId: str = Field(..., description="ID of the aggregate")
    valueObjectId: str = Field(..., description="ID of the value object")

class ActionArgs(BaseModelWithItem):
    """Arguments for the value object creation action"""
    fromAggregate: str = Field(..., description="The name of the aggregate that contains this value object reference.")
    toAggregate: str = Field(..., description="The name of the aggregate being referenced.")
    valueObjectName: str = Field(..., description="Name of the value object")
    referenceClass: str = Field(..., description="Name of the referenced class")
    properties: List[PropertyOutput] = Field(..., description="List of properties for the value object")

class ActionOutput(BaseModelWithItem):
    """Single action to create a value object"""
    inference: str = Field(..., description="Inference for creating this specific value object reference.")
    objectType: str = Field(..., description="Type of object to create (ValueObject)")
    ids: ActionIds = Field(..., description="Target identifiers for the action")
    args: ActionArgs = Field(..., description="Arguments for creating the value object")

class OmittedReferenceOutput(BaseModelWithItem):
    """Describes a reference that was intentionally omitted to enforce unidirectional relationships."""
    fromAggregate: str = Field(..., description="The aggregate where the reference would have originated.")
    toAggregate: str = Field(..., description="The aggregate that would have been referenced.")
    reason: str = Field(..., description="Justification for omitting this reference, based on DDD principles (e.g., lifecycle dependency, stability).")

class ResultOutput(BaseModelWithItem):
    """Result containing the actions to perform"""
    omittedReferences: List[OmittedReferenceOutput] = Field(..., description="List of references that were intentionally omitted to avoid bidirectional dependencies.")
    actions: List[ActionOutput] = Field(..., description="List of actions to create value objects")

class CreateAggregateClassIdByDraftsOutput(BaseModelWithItem):
    """Output model for creating aggregate class references by drafts"""
    inference: str = Field(..., description="Reasoning and analysis for the design decisions")
    result: ResultOutput = Field(..., description="The resulting actions to create value objects and the list of omitted references.")