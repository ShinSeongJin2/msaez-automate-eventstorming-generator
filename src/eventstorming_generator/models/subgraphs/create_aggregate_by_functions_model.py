from typing import Dict, Any, List
from pydantic import Field

from ..base import BaseModelWithItem
from ..action_model import ActionModel

class AggregateGenerationState(BaseModelWithItem):
    """단일 Aggregate 생성 처리 상태"""
    target_bounded_context: Dict[str, Any] = Field(default_factory=dict)
    target_aggregate: Dict[str, Any] = Field(default_factory=dict)
    description: str = ""
    original_description: str = ""
    requirements: Dict[str, Any] = Field(default_factory=dict)
    draft_option: List[Dict[str, Any]] = Field(default_factory=list)
    retry_count: int = 0
    created_actions: List[ActionModel] = Field(default_factory=list)
    generation_complete: bool = False
    extracted_ddl_fields: List[str] = Field(default_factory=list)
    missing_ddl_fields: List[str] = Field(default_factory=list)
    ddl_extraction_attempted: bool = False
    ddl_fields: List[str] = Field(default_factory=list)
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