from typing import Dict, List, Optional
from pydantic import Field

from .base import BaseModelWithItem
from ..types import RequirementIndexMapping
from .es_models import BoundedContextStructureModel

class IdsModel(BaseModelWithItem):
    projectId: str = None
    uid: str = None

class AdditionalRequestsModel(BaseModelWithItem):
    essentialAggregateAttributes: Optional[Dict[str, Dict[str, List[str]]]] = None
    essentialCommandNames: Optional[Dict[str, List[str]]] = None
    essentialEventNames: Optional[Dict[str, List[str]]] = None
    essentialReadModelNames: Optional[Dict[str, List[str]]] = None

class MetadatasModel(BaseModelWithItem):
    boundedContextRequirements: Dict[str, str] = Field(default_factory=dict)
    boundedContextRequirementIndexMapping: Dict[str, RequirementIndexMapping] = Field(default_factory=dict)

class DraftModel(BaseModelWithItem):
    additionalRequests: AdditionalRequestsModel = Field(default_factory=AdditionalRequestsModel)
    metadatas: MetadatasModel = Field(default_factory=MetadatasModel)
    structures: List[BoundedContextStructureModel] = Field(default_factory=list)

class InputsModel(BaseModelWithItem):
    requestType: str = None
    jobId: str = ""
    ids: IdsModel = Field(default_factory=IdsModel)
    draft: Optional[DraftModel] = None
    requirements: Optional[str] = None
    preferedLanguage: str = "English"

    after_stop_node: Optional[str] = None # 디버깅 전용
