from typing import Dict, List
from pydantic import Field

from ..base import BaseModelWithItem
from ..es_models import BoundedContextInfoModel

class BoundedContextGenerationState(BaseModelWithItem):
    """단일 Bounded Context 생성 처리 상태"""
    requirements: str = ""
    created_bounded_contexts: List[BoundedContextInfoModel] = Field(default_factory=list)
    worker_index: int = 0

    retry_count: int = 0
    generation_complete: bool = False
    is_preprocess_completed: bool = False
    is_failed: bool = False

class CreateBoundedContextByFunctionsModel(BaseModelWithItem):
    """Bounded Context 생성 관련 상태 관리 모델"""
    worker_generations: Dict[str, BoundedContextGenerationState] = Field(default_factory=dict)
    
    current_batch: List[BoundedContextGenerationState] = Field(default_factory=list)
    parallel_worker_results: List[BoundedContextGenerationState] = Field(default_factory=list)
    
    completed_generations: List[BoundedContextGenerationState] = Field(default_factory=list)
    pending_generations: List[BoundedContextGenerationState] = Field(default_factory=list)
    
    is_processing: bool = False
    all_complete: bool = False
    is_merge_completed: bool = False
    
    max_retry_count: int = 3
    is_failed: bool = False

    total_seconds: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0

    accumulated_bounded_contexts: List[BoundedContextInfoModel] = Field(default_factory=list)
    merged_bounded_contexts: List[BoundedContextInfoModel] = Field(default_factory=list)