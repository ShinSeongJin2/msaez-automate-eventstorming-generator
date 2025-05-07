from pydantic import BaseModel
from typing import Optional

class UserInfoModel(BaseModel):
    name: Optional[str] = None
    profile: Optional[str] = None
    email: Optional[str] = None
    uid: Optional[str] = None
    providerUid: Optional[str] = None
    savedCoin: Optional[int] = None
    savedToolTime: Optional[int] = None
    consultingTime: Optional[int] = None
    authorized: Optional[str] = None 