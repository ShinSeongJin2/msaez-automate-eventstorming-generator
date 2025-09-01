from pydantic import Field
from typing import List, Optional, Union
from ..base import BaseModelWithItem

Refs = Optional[List[List[List[Union[int, str]]]]]

class PropertyAssignment(BaseModelWithItem):
    """Model representing a single property assignment"""
    name: str = Field(..., description="Name of the field to be added.")
    type: str = Field(..., description="Inferred data type for the field (e.g., String, Long, Date). Default to String if unsure.")
    refs: Refs = Field(None, description="Source reference from the functional requirements")

class ParentAssignment(BaseModelWithItem):
    """Model for assigning a list of properties to a specific parent (Aggregate or ValueObject)"""
    parent_type: str = Field(..., description="Type of the parent, either 'Aggregate' or 'ValueObject'.")
    parent_id: str = Field(..., description="The unique ID of the parent element (aggregateId or valueObjectId).")
    parent_name: str = Field(..., description="The name of the parent element.")
    properties_to_add: List[PropertyAssignment] = Field(..., description="List of properties to add to this parent.")

class AssignFieldsToActionsGeneratorResult(BaseModelWithItem):
    """Model for assigning a list of properties to a specific parent (Aggregate or ValueObject)"""
    assignments: List[ParentAssignment] = Field(..., description="List of parent elements with the new fields assigned to them.")
    invalid_properties: List[str] = Field(default_factory=list, description="List of properties that are commented out or invalid and therefore cannot be assigned")

class AssignFieldsToActionsGeneratorOutput(BaseModelWithItem):
    """Structured Output Model of the AssignFieldsToActionsGenerator"""
    inference: str = Field(..., description="Reasoning for why each field was assigned to its respective parent.")
    result: AssignFieldsToActionsGeneratorResult = Field(..., description="The result of the assign fields to actions generator.") 