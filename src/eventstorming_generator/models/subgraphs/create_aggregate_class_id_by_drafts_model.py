from typing import Dict, Any, List, Optional
from pydantic import Field

from ..base import BaseModelWithItem
from ..action_model import ActionModel

class ClassIdGenerationState(BaseModelWithItem):
    """단일 Aggregate 클래스 ID 생성 처리 상태"""
    target_references: List[str] = Field(default_factory=list)
    draft_option: Dict[str, Any] = Field(default_factory=dict)
    summarized_es_value: Dict[str, Any] = Field(default_factory=dict)
    created_actions: List[ActionModel] = Field(default_factory=list)
    retry_count: int = 0
    generation_complete: bool = False
    is_token_over_limit: bool = False

class CreateAggregateClassIdByDraftsModel(BaseModelWithItem):
    """Aggregate 클래스 ID 생성 관련 상태 관리 모델"""
    draft_options: Dict[str, Any] = Field(default_factory=dict)
    current_generation: Optional[ClassIdGenerationState] = None
    completed_generations: List[ClassIdGenerationState] = Field(default_factory=list)
    pending_generations: List[ClassIdGenerationState] = Field(default_factory=list)
    
    is_processing: bool = False
    all_complete: bool = False
    
    max_retry_count: int = 3
    is_failed: bool = False

    total_seconds: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0