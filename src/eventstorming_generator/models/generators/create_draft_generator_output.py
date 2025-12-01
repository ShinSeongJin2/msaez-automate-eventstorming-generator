from typing import List
from pydantic import Field

from ..base import BaseModelWithItem
from ..es_models import AggregateInfoNoRefModel

class CreateDraftGeneratorOutput(BaseModelWithItem):
    """Create Draft Generator Output"""
    aggregates: List[AggregateInfoNoRefModel] = Field(..., description="List of aggregate structures")