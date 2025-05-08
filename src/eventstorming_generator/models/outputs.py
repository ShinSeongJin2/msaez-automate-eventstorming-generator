from pydantic import BaseModel
from typing import Any

class OutputsModel(BaseModel):
    esValue: Any = None
