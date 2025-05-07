from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class BoundedContextElementView(BaseModel):
    _type: Optional[str] = None
    height: Optional[int] = None
    id: Optional[str] = None
    style: Optional[str] = None
    width: Optional[int] = None
    x: Optional[int] = None
    y: Optional[int] = None

class BoundedContextHexagonalView(BaseModel):
    _type: Optional[str] = None
    height: Optional[int] = None
    id: Optional[str] = None
    style: Optional[str] = None
    width: Optional[int] = None
    x: Optional[int] = None
    y: Optional[int] = None

class BoundedContextModel(BaseModel):
    _type: Optional[str] = None
    aggregates: Optional[List[Any]] = Field(default_factory=list) # Further nesting can be defined if needed
    author: Optional[str] = None
    description: Optional[str] = None # This can be a JSON string
    id: Optional[str] = None
    elementView: Optional[BoundedContextElementView] = None
    gitURL: Optional[str] = None
    hexagonalView: Optional[BoundedContextHexagonalView] = None
    members: Optional[List[Any]] = Field(default_factory=list)
    name: Optional[str] = None
    displayName: Optional[str] = None
    oldName: Optional[str] = None
    policies: Optional[List[Any]] = Field(default_factory=list)
    portGenerated: Optional[int] = None
    preferredPlatform: Optional[str] = None
    preferredPlatformConf: Optional[Dict[str, Any]] = Field(default_factory=dict)
    rotateStatus: Optional[bool] = None
    tempId: Optional[str] = None
    templatePerElements: Optional[Dict[str, Any]] = Field(default_factory=dict)
    views: Optional[List[Any]] = Field(default_factory=list)
    definitionId: Optional[str] = None
