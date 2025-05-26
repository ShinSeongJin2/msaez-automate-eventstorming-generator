from datetime import datetime
from pydantic import ConfigDict
from typing import Any, Dict, List

from .base import BaseModelWithItem

class LogModel(BaseModelWithItem):
    created_at: str = datetime.now().isoformat()
    level: str = ""
    message: str = ""
    model_config = ConfigDict(extra="allow")

class EsValueModel(BaseModelWithItem):
    elements: Dict[str, Any] = {}
    relations: Dict[str, Any] = {}
    model_config = ConfigDict(extra="allow")

class OutputsModel(BaseModelWithItem):
    esValue: EsValueModel = EsValueModel()
    isCompleted: bool = False
    logs: List[LogModel] = []
    totalProgressCount: int = 0
    currentProgressCount: int = 0
