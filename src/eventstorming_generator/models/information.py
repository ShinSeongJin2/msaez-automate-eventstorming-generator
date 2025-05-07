from pydantic import BaseModel
from typing import Optional

class InformationModel(BaseModel):
    author: Optional[str] = None
    authorEmail: Optional[str] = None
    comment: Optional[str] = None
    createdTimeStamp: Optional[int] = None
    lastModifiedTimeStamp: Optional[int] = None
    projectName: Optional[str] = None
    projectId: Optional[str] = None
    type: Optional[str] = None 