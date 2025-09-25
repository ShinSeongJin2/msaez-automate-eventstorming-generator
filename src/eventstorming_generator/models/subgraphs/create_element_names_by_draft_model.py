from typing import Dict, Any, List, Optional
from pydantic import Field

from ..base import BaseModelWithItem

class ExtractedElementNameDetail(BaseModelWithItem):
    """Extracted Element Name Details"""
    command_names: List[str] = Field(default_factory=list)
    event_names: List[str] = Field(default_factory=list)
    read_model_names: List[str] = Field(default_factory=list)

class ElementNamesGenerationState(BaseModelWithItem):
    """단일 BoundedContext에 대한 Element Names 생성 처리 상태"""
    previousElementNames: Dict[str, Dict[str, ExtractedElementNameDetail]] = Field(default_factory=dict)
    target_bounded_context_name: str = Field(default_factory=str)
    aggregate_draft: List[Dict[str, Any]] = Field(default_factory=list)
    description: str = ""
    requested_event_names: List[str] = Field(default_factory=list)
    requested_command_names: List[str] = Field(default_factory=list)
    requested_read_model_names: List[str] = Field(default_factory=list)

    retry_count: int = 0
    generation_complete: bool = False
    extracted_element_names: Dict[str, ExtractedElementNameDetail] = Field(default_factory=dict)
    is_preprocess_completed: bool = False

class CreateElementNamesByDraftsModel(BaseModelWithItem):
    """BoundedContext에 대한 Element Names 생성 관련 상태 관리 모델"""
    current_generation: Optional[ElementNamesGenerationState] = None
    completed_generations: List[ElementNamesGenerationState] = Field(default_factory=list)
    pending_generations: List[ElementNamesGenerationState] = Field(default_factory=list)

    is_processing: bool = False
    all_complete: bool = False
    
    max_retry_count: int = 3
    is_failed: bool = False

    total_seconds: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0

    extracted_element_names: Dict[str, Dict[str, ExtractedElementNameDetail]] = Field(default_factory=dict)