from typing import List, Dict, Any

from pydantic import Field

from ..base import BaseModelWithItem
from ..action_model import ActionModel

class CreateUiComponentsGenerationState(BaseModelWithItem):
    """단일 UIComponents 생성 처리 상태"""
    target_ui_component: Dict[str, Any] = Field(default_factory=dict)
    ai_request_type: str = ""
    ai_input_data: Dict[str, Any] = Field(default_factory=dict)
    ui_replace_actions: List[ActionModel] = Field(default_factory=list)
    worker_index: int = 0
    
    retry_count: int = 0
    generation_complete: bool = False
    is_failed: bool = False

class CreateUiComponentsModel(BaseModelWithItem):
    """UIComponents 생성 관련 상태 관리 모델"""
    worker_generations: Dict[str, CreateUiComponentsGenerationState] = Field(default_factory=dict)
    
    current_batch: List[CreateUiComponentsGenerationState] = Field(default_factory=list)
    parallel_worker_results: List[CreateUiComponentsGenerationState] = Field(default_factory=list)
    
    completed_generations: List[CreateUiComponentsGenerationState] = Field(default_factory=list)    
    pending_generations: List[CreateUiComponentsGenerationState] = Field(default_factory=list)
    
    is_processing: bool = False
    all_complete: bool = False
    
    max_retry_count: int = 3
    is_failed: bool = False

    total_seconds: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0