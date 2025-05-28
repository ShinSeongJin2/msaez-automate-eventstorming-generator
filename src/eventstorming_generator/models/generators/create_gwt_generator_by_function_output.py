from pydantic import Field
from typing import List, Dict, Any
from ..base import BaseModelWithItem

class GWTStep(BaseModelWithItem):
    """Represents a single step in a Given-When-Then scenario"""
    name: str = Field(description="Name of the step (Aggregate, Command, or Event name)")
    values: Dict[str, Any] = Field(description="Attribute values for the step, can contain actual values, null, or 'N/A'")

class GWTScenario(BaseModelWithItem):
    """Represents a complete Given-When-Then test scenario"""
    given: GWTStep = Field(description="Given step representing the initial Aggregate state")
    when: GWTStep = Field(description="When step representing the Command being executed")
    then: GWTStep = Field(description="Then step representing the expected Event outcome")

class CommandGWT(BaseModelWithItem):
    """Represents GWT scenarios for a specific target command"""
    targetCommandId: str = Field(description="ID of the target command for which GWT scenarios are generated")
    gwts: List[GWTScenario] = Field(description="List of GWT scenarios for the target command")

class CreateGWTGeneratorByFunctionOutput(BaseModelWithItem):
    """Output model for CreateGWTGeneratorByFunction containing inference and GWT scenarios"""
    inference: str = Field(description="Detailed reasoning and analysis behind the generated GWT scenarios")
    result: List[CommandGWT] = Field(description="List of commands with their associated GWT scenarios")