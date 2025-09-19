from pydantic import Field
from typing import List, Dict, Any
from ..base import BaseModelWithItem

class GivenStep(BaseModelWithItem):
    """Represents the Given step in a GWT scenario with Aggregate information"""
    aggregateName: str = Field(description="Name of the Aggregate")
    aggregateValues: Dict[str, Any] = Field(description="Attribute values for the Aggregate, must be a non-empty dictionary with actual values")

class WhenStep(BaseModelWithItem):
    """Represents the When step in a GWT scenario with Command information"""
    commandName: str = Field(description="Name of the Command")
    commandValues: Dict[str, Any] = Field(description="Parameter values for the Command, must be a non-empty dictionary with actual values")

class ThenStep(BaseModelWithItem):
    """Represents the Then step in a GWT scenario with Event information"""
    eventName: str = Field(description="Name of the Event")
    eventValues: Dict[str, Any] = Field(description="Property values for the Event, must be a non-empty dictionary with actual values")

class GWTScenario(BaseModelWithItem):
    """Represents a complete Given-When-Then test scenario"""
    scenario: str = Field(description="Brief description of what business scenario this GWT test validates")
    given: GivenStep = Field(description="Given step representing the initial Aggregate state")
    when: WhenStep = Field(description="When step representing the Command being executed")
    then: ThenStep = Field(description="Then step representing the expected Event outcome")

class GWTResult(BaseModelWithItem):
    """Represents GWT scenarios for a single command"""
    gwts: List[GWTScenario] = Field(description="List of GWT scenarios for the command")

class CreateGWTGeneratorByFunctionOutput(BaseModelWithItem):
    """Output model for CreateGWTGeneratorByFunction containing inference and GWT scenarios"""
    inference: str = Field(description="Detailed reasoning and analysis behind the generated GWT scenarios")
    result: GWTResult = Field(description="GWT scenarios for the command")