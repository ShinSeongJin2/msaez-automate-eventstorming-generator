from typing import List
from pydantic import Field
from ..base import BaseModelWithItem
from ..es_models import BoundedContextInfoModel

class MergeCreatedBoundedContextGeneratorOutput(BaseModelWithItem):
    """Merged Bounded Context Generator Output"""
    mergedBoundedContexts: List[BoundedContextInfoModel] = Field(..., description="List of merged bounded contexts")