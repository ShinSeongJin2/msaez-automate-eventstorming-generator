from pydantic import Field
from typing import List
from ..base import BaseModelWithItem

class ESValueSummaryGeneratorOutput(BaseModelWithItem):
    """Output model for Event Storming value summary generator"""
    sortedElementIds: List[str] = Field(
        ...,
        description="List of Event Storming element IDs sorted by relevance to the given context"
    )