from pydantic import Field
from typing import List
from ..base import BaseModelWithItem

class GivenStep(BaseModelWithItem):
    """Represents the Given step in a GWT scenario with Aggregate information"""
    aggregateName: str = Field(..., description="Name of the Aggregate")
    aggregateValues: str = Field(..., description="A JSON string representing attribute values for the Aggregate. Must be a non-empty JSON object with actual values.")

class WhenStep(BaseModelWithItem):
    """Represents the When step in a GWT scenario with Command information"""
    commandName: str = Field(..., description="Name of the Command")
    commandValues: str = Field(..., description="A JSON string representing parameter values for the Command. Must be a non-empty JSON object with actual values.")

class ThenStep(BaseModelWithItem):
    """Represents the Then step in a GWT scenario with Event information"""
    eventName: str = Field(..., description="Name of the Event")
    eventValues: str = Field(..., description="A JSON string representing property values for the Event. Must be a non-empty JSON object with actual values.")

class GWTScenario(BaseModelWithItem):
    """Represents a complete Given-When-Then test scenario"""
    scenario: str = Field(..., description="Brief description of what business scenario this GWT test validates")
    given: GivenStep = Field(..., description="Given step representing the initial Aggregate state")
    when: WhenStep = Field(..., description="When step representing the Command being executed")
    then: ThenStep = Field(..., description="Then step representing the expected Event outcome")

class CreateGWTGeneratorByFunctionOutput(BaseModelWithItem):
    """Output model for CreateGWTGeneratorByFunction containing GWT scenarios"""
    gwts: List[GWTScenario] = Field(..., description="List of GWT scenarios for the command")