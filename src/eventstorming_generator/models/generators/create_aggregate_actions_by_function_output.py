from pydantic import Field
from typing import List, Optional
from ..base import BaseModelWithItem

Refs = List[List[List[str]]]

class EnumPropertyModel(BaseModelWithItem):
    """Model representing a property of an enumeration"""
    name: str = Field(..., description="Name of the property")
    refs: Refs = Field(..., description="Source reference from the functional requirements")

class PropertyModel(BaseModelWithItem):
    """Model representing a property of an aggregate, value object"""
    name: str = Field(..., description="Name of the property")
    type: Optional[str] = Field(None, description="Type of the property (optional for String type)")
    isKey: Optional[bool] = Field(None, description="Whether this property is a primary key")
    isForeignProperty: Optional[bool] = Field(None, description="Whether this property is a foreign key reference")
    refs: Refs = Field(..., description="Source reference from the functional requirements")

class AggregateIds(BaseModelWithItem):
    """Model representing aggregate identifiers"""
    aggregateId: str = Field(..., description="Unique identifier for the aggregate")

class ValueObjectIds(BaseModelWithItem):
    """Model representing value object identifiers"""
    aggregateId: str = Field(..., description="Aggregate identifier this value object belongs to")
    valueObjectId: str = Field(..., description="Unique identifier for the value object")

class EnumerationIds(BaseModelWithItem):
    """Model representing enumeration identifiers"""
    aggregateId: str = Field(..., description="Aggregate identifier this enumeration belongs to")
    enumerationId: str = Field(..., description="Unique identifier for the enumeration")

class AggregateArgs(BaseModelWithItem):
    """Model representing arguments for aggregate creation"""
    aggregateName: str = Field(..., description="Name of the aggregate")
    aggregateAlias: str = Field(..., description="Human-readable alias for the aggregate")
    properties: List[PropertyModel] = Field(..., description="List of properties for the aggregate", min_length=1)
    refs: Refs = Field(..., description="Source reference from the functional requirements")

class ValueObjectArgs(BaseModelWithItem):
    """Model representing arguments for value object creation"""
    valueObjectName: str = Field(..., description="Name of the value object")
    valueObjectAlias: str = Field(..., description="Human-readable alias for the value object")
    properties: List[PropertyModel] = Field(..., description="List of properties for the value object", min_length=1)
    refs: Refs = Field(..., description="Source reference from the functional requirements")

class EnumerationArgs(BaseModelWithItem):
    """Model representing arguments for enumeration creation"""
    enumerationName: str = Field(..., description="Name of the enumeration")
    enumerationAlias: str = Field(..., description="Human-readable alias for the enumeration")
    properties: List[EnumPropertyModel] = Field(..., description="List of enumeration values", min_length=1)
    refs: Refs = Field(..., description="Source reference from the functional requirements")

class AggregateAction(BaseModelWithItem):
    """Model representing an aggregate creation action"""
    actionName: str = Field(..., description="Name of the action being performed")
    objectType: str = Field(..., description="Type of object (should be 'Aggregate')")
    ids: AggregateIds = Field(..., description="Identifiers for the aggregate")
    args: AggregateArgs = Field(..., description="Arguments for aggregate creation")

class ValueObjectAction(BaseModelWithItem):
    """Model representing a value object creation action"""
    actionName: str = Field(..., description="Name of the action being performed")
    objectType: str = Field(..., description="Type of object (should be 'ValueObject')")
    ids: ValueObjectIds = Field(..., description="Identifiers for the value object")
    args: ValueObjectArgs = Field(..., description="Arguments for value object creation")

class EnumerationAction(BaseModelWithItem):
    """Model representing an enumeration creation action"""
    actionName: str = Field(..., description="Name of the action being performed")
    objectType: str = Field(..., description="Type of object (should be 'Enumeration')")
    ids: EnumerationIds = Field(..., description="Identifiers for the enumeration")
    args: EnumerationArgs = Field(..., description="Arguments for enumeration creation")

class CreateAggregateActionsByFunctionOutput(BaseModelWithItem):
    """Structured Output Model of the CreateAggregateActionsByFunction Generator"""
    aggregateActions: List[AggregateAction] = Field(..., description="List of aggregate creation actions")
    valueObjectActions: List[ValueObjectAction] = Field(..., description="List of value object creation actions")
    enumerationActions: List[EnumerationAction] = Field(..., description="List of enumeration creation actions")
    