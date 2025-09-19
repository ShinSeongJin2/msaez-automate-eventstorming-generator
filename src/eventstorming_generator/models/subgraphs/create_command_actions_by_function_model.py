from typing import Dict, Any, List, Optional
from pydantic import Field

from ..base import BaseModelWithItem
from ..action_model import ActionModel

class CommandActionGenerationState(BaseModelWithItem):
    """단일 Aggregate에 대한 Command 액션 생성 처리 상태"""
    target_bounded_context: Dict[str, Any] = Field(default_factory=dict)
    target_aggregate: Dict[str, Any] = Field(default_factory=dict)
    description: str = ""
    original_description: str = ""
    summarized_es_value: Dict[str, Any] = Field(default_factory=dict)
    retry_count: int = 0
    created_actions: List[ActionModel] = Field(default_factory=list)
    generation_complete: bool = False
    is_token_over_limit: bool = False
    required_event_names: List[str] = Field(default_factory=list)
    extractedElementNames: List[Any] = Field(default_factory=list)

class CreateCommandActionsByFunctionModel(BaseModelWithItem):
    """Command 액션 생성 관련 상태 관리 모델"""
    draft_options: Dict[str, Any] = Field(default_factory=dict)
    current_generation: Optional[CommandActionGenerationState] = None
    completed_generations: List[CommandActionGenerationState] = Field(default_factory=list)
    pending_generations: List[CommandActionGenerationState] = Field(default_factory=list)
    
    is_processing: bool = False
    all_complete: bool = False
    
    max_retry_count: int = 3
    is_failed: bool = False

    assign_event_names_complete: bool = False

    total_seconds: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0