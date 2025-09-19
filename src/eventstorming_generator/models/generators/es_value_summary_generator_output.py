from pydantic import Field
from typing import List
from ..base import BaseModelWithItem

class ESValueSummaryResult(BaseModelWithItem):
    """Result model for Event Storming value summary generation containing sorted element IDs"""
    sortedElementIds: List[str] = Field(
        ...,
        description="List of Event Storming element IDs sorted by relevance to the given context"
    )

class ESValueSummaryGeneratorOutput(BaseModelWithItem):
    """Output model for Event Storming value summary generator"""
    result: ESValueSummaryResult = Field(
        ...,
        description="The result containing sorted Event Storming element IDs"
    )