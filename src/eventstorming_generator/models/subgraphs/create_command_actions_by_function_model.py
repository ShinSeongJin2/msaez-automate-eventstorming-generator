from typing import Dict, Any, List
from pydantic import Field

from ..base import BaseModelWithItem
from ..action_model import ActionModel
from ..subgraphs.create_element_names_by_draft_model import ExtractedElementNameDetail

class CommandActionGenerationState(BaseModelWithItem):
    """단일 Aggregate에 대한 Command 액션 생성 처리 상태"""
    target_bounded_context_name: str = Field(default_factory=str)
    target_aggregate_name: str = Field(default_factory=str)
    description: str = ""
    original_description: str = ""
    extracted_element_names: ExtractedElementNameDetail = Field(default_factory=ExtractedElementNameDetail)
    summarized_es_value: Dict[str, Any] = Field(default_factory=dict)

    retry_count: int = 0
    created_actions: List[ActionModel] = Field(default_factory=list)
    generation_complete: bool = False
    is_failed: bool = False

class CreateCommandActionsByFunctionModel(BaseModelWithItem):
    """Command 액션 생성 관련 상태 관리 모델"""
    completed_generations: List[CommandActionGenerationState] = Field(default_factory=list)
    pending_generations: List[CommandActionGenerationState] = Field(default_factory=list)
    
    worker_generations: Dict[str, CommandActionGenerationState] = Field(default_factory=dict)
    current_batch: List[CommandActionGenerationState] = Field(default_factory=list)
    parallel_worker_results: List[CommandActionGenerationState] = Field(default_factory=list)
    
    is_processing: bool = False
    all_complete: bool = False
    
    max_retry_count: int = 3
    is_failed: bool = False

    total_seconds: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0