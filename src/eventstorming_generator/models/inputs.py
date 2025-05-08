from typing import Any
from pydantic import BaseModel, ConfigDict

class UserInfoModel(BaseModel):
    uid: str
    model_config = ConfigDict(extra="allow")

class InformationModel(BaseModel):
    projectId: str
    model_config = ConfigDict(extra="allow")

class InputsModel(BaseModel):
    selectedDraftOptions: Any = None
    userInfo: UserInfoModel = None
    information: InformationModel = None