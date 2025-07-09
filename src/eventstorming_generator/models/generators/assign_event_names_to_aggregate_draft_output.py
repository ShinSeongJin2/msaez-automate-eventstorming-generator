from pydantic import Field
from typing import List
from ..base import BaseModelWithItem

class AggregateEventAssignment(BaseModelWithItem):
    """Represents the assignment of events to a specific aggregate"""
    aggregateName: str = Field(description="Name of the aggregate")
    eventNames: List[str] = Field(description="List of event names assigned to this aggregate")

class AssignEventNamesToAggregateDraftOutput(BaseModelWithItem):
    """Output model for assigning event names to aggregates with structured reasoning and results"""
    inference: str = Field(description="Detailed reasoning and analysis for the event assignments")
    result: List[AggregateEventAssignment] = Field(description="List of aggregates with their assigned event names") 