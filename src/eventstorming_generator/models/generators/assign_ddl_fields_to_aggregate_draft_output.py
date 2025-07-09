from pydantic import Field
from typing import List
from ..base import BaseModelWithItem

class AggregateFieldAssignment(BaseModelWithItem):
    """Model representing DDL field assignment to a specific aggregate"""
    aggregateName: str = Field(..., description="Name of the aggregate to assign fields to")
    ddl_fields: List[str] = Field(..., description="List of DDL field names assigned to this aggregate")

class AssignDDLFieldsToAggregateDraftResult(BaseModelWithItem):
    """Model representing the result of DDL field assignments"""
    aggregateFieldAssignments: List[AggregateFieldAssignment] = Field(..., description="List of aggregates with their assigned DDL fields")

class AssignDDLFieldsToAggregateDraftOutput(BaseModelWithItem):
    """Structured Output Model of the AssignDDLFieldsToAggregateDraft Generator"""
    inference: str = Field(..., description="Reasoning for the field assignments, including analysis of domain context and assignment decisions")
    result: AssignDDLFieldsToAggregateDraftResult = Field(..., description="The result containing DDL field assignments for each aggregate") 