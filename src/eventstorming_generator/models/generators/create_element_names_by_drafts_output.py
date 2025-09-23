from pydantic import Field
from typing import Dict
from ..base import BaseModelWithItem
from ..subgraphs.create_element_names_by_draft_model import ExtractedElementNameDetail

class CreateElementNamesByDraftsResult(BaseModelWithItem):
    extracted_element_names: Dict[str, ExtractedElementNameDetail] = Field(default_factory=dict, description="Generated element names for aggregates.")

class CreateElementNamesByDraftsOutput(BaseModelWithItem):
    """Structured Output Model of the CreateElementNamesByDrafts Generator"""
    inference: str = Field(..., description="Reasoning and analysis behind the design decisions")
    result: CreateElementNamesByDraftsResult = Field(..., description="Generated element names for aggregates, value objects, and enumerations")
    