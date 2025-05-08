from pydantic import BaseModel, ConfigDict
from typing import Any, Dict

class EsValueModel(BaseModel):
    elements: Dict[str, Any] = {}
    relations: Dict[str, Any] = {}
    model_config = ConfigDict(extra="allow")

class OutputsModel(BaseModel):
    esValue: EsValueModel = EsValueModel()
