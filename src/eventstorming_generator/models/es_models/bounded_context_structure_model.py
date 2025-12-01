from typing import List
from pydantic import Field

from ..base import BaseModelWithItem
from .aggregate_info_model import AggregateInfoModel

class BoundedContextStructureModel(BaseModelWithItem):
    boundedContextAlias: str = None
    boundedContextName: str = None
    aggregates: List[AggregateInfoModel] = Field(default_factory=list)