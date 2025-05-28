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
    valueObjectName: str = Field(..., description="Name of the value object")
    referenceClass: str = Field(..., description="Name of the referenced class")
    properties: List[PropertyOutput] = Field(..., description="List of properties for the value object")

class ActionOutput(BaseModelWithItem):
    """Single action to create a value object"""
    objectType: str = Field(..., description="Type of object to create (ValueObject)")
    ids: ActionIds = Field(..., description="Target identifiers for the action")
    args: ActionArgs = Field(..., description="Arguments for creating the value object")

class ResultOutput(BaseModelWithItem):
    """Result containing the actions to perform"""
    actions: List[ActionOutput] = Field(..., description="List of actions to create value objects")

class CreateAggregateClassIdByDraftsOutput(BaseModelWithItem):
    """Output model for creating aggregate class references by drafts"""
    inference: str = Field(..., description="Reasoning and analysis for the design decisions")
    result: ResultOutput = Field(..., description="The resulting actions to create value objects")