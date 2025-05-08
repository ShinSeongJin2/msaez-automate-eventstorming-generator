from pydantic import ConfigDict
from typing import Any, Dict

from .base import BaseModelWithItem

class EsValueModel(BaseModelWithItem):
    elements: Dict[str, Any] = {}
    relations: Dict[str, Any] = {}
    model_config = ConfigDict(extra="allow")

class OutputsModel(BaseModelWithItem):
    esValue: EsValueModel = EsValueModel()
