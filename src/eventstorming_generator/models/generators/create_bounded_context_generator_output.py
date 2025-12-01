from typing import List
from pydantic import Field
from ..base import BaseModelWithItem
from ..es_models import BoundedContextInfoModel

class CreateBoundedContextGeneratorOutput(BaseModelWithItem):
    """Bounded Context Generator Output"""
    boundedContexts: List[BoundedContextInfoModel] = Field(..., description="List of created bounded contexts")