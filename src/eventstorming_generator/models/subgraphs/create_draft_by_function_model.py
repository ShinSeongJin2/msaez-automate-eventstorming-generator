from typing import Dict, List, Optional
from pydantic import Field

from ..base import BaseModelWithItem
from ..es_models import BoundedContextInfoModel
from ..inputs import BoundedContextStructureModel

class DraftGenerationState(BaseModelWithItem):
    """단일 Bounded Context 생성 처리 상태"""
    bounded_context_info: BoundedContextInfoModel = Field(default_factory=BoundedContextInfoModel)
    requirements: str = ""
    
    created_draft: Optional[BoundedContextStructureModel] = None
    worker_index: int = 0

    retry_count: int = 0
    generation_complete: bool = False
    is_preprocess_completed: bool = False
    is_failed: bool = False

class CreateDraftByFunctionModel(BaseModelWithItem):
    """Bounded Context 생성 관련 상태 관리 모델"""
    worker_generations: Dict[str, DraftGenerationState] = Field(default_factory=dict)
    
    current_batch: List[DraftGenerationState] = Field(default_factory=list)
    parallel_worker_results: List[DraftGenerationState] = Field(default_factory=list)
    
    completed_generations: List[DraftGenerationState] = Field(default_factory=list)
    pending_generations: List[DraftGenerationState] = Field(default_factory=list)
    
    is_processing: bool = False
    all_complete: bool = False
    is_merge_completed: bool = False
    
    max_retry_count: int = 3
    is_failed: bool = False

    total_seconds: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0

    accumulated_drafts: List[BoundedContextStructureModel] = Field(default_factory=list)