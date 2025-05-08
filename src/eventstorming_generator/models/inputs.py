from typing import Any
from pydantic import BaseModel

class InputsModel(BaseModel):
    selectedDraftOptions: Any = None
    userInfo: Any = None
    information: Any = None
