from typing import Dict, List, Optional
from pydantic import Field

from ..base import BaseModelWithItem
from ..action_model import ActionModel
from ..es_models import AggregateInfoModel
from ...types import RequirementIndexMapping

class AggregateGenerationState(BaseModelWithItem):
    """단일 Aggregate 생성 처리 상태"""
    target_bounded_context_name: str = ""
    target_aggregate_structure: AggregateInfoModel = Field(default_factory=AggregateInfoModel)
    description: str = ""
    original_description: str = ""
    requirement_index_mapping: Optional[RequirementIndexMapping] = None
    worker_index: int = 0

    attributes_to_generate: List[str] = Field(default_factory=list)
    missing_attributes: List[str] = Field(default_factory=list)

    created_actions: List[ActionModel] = Field(default_factory=list)

    retry_count: int = 0
    generation_complete: bool = False
    is_preprocess_completed: bool = False
    is_action_postprocess_completed: bool = False
    is_failed: bool = False

class CreateAggregateByFunctionsModel(BaseModelWithItem):
    """Aggregate 생성 관련 상태 관리 모델"""
    worker_generations: Dict[str, AggregateGenerationState] = Field(default_factory=dict)
    
    current_batch: List[AggregateGenerationState] = Field(default_factory=list)
    parallel_worker_results: List[AggregateGenerationState] = Field(default_factory=list)
    
    completed_generations: List[AggregateGenerationState] = Field(default_factory=list)
    pending_generations: List[AggregateGenerationState] = Field(default_factory=list)
    
    is_processing: bool = False
    all_complete: bool = False
    
    max_retry_count: int = 3
    is_failed: bool = False

    total_seconds: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0