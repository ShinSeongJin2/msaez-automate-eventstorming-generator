from typing import Any, Dict
from pydantic import ConfigDict

from .base import BaseModelWithItem

class UserInfoModel(BaseModelWithItem):
    uid: str
    model_config = ConfigDict(extra="allow")

class InformationModel(BaseModelWithItem):
    projectId: str
    model_config = ConfigDict(extra="allow")

class LLMModel(BaseModelWithItem):
    model_vendor: str = "openai"
    model_name: str = "gpt-4.1-2025-04-14"
    model_kwargs: Dict[str, Any] = {}
    model_max_input_limit: int = 962429
    api_key: str = ""

class InputsModel(BaseModelWithItem):
    selectedDraftOptions: Any = None
    userInfo: UserInfoModel = None
    information: InformationModel = None
    llmModel: LLMModel = LLMModel()
    preferedLanguage: str = "Korean"