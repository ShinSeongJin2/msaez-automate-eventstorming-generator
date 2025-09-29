from pydantic import Field
from typing import List
from ..base import BaseModelWithItem

class AggregateElementNames(BaseModelWithItem):
    """Element names for a single aggregate"""
    aggregate_name: str = Field(..., description="Name of the aggregate.")
    command_names: List[str] = Field(default_factory=list, description="List of command names.")
    event_names: List[str] = Field(default_factory=list, description="List of event names.")
    read_model_names: List[str] = Field(default_factory=list, description="List of read model names.")

class CreateElementNamesByDraftsOutput(BaseModelWithItem):
    """Structured Output Model of the CreateElementNamesByDrafts Generator"""
    extracted_element_names: List[AggregateElementNames] = Field(..., description="Generated element names for aggregates.")
    