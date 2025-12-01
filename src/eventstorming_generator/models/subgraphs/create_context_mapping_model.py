from typing import Dict, List
from pydantic import Field

from ..base import BaseModelWithItem
from ..es_models import BoundedContextInfoModel
from ..generators import ContextMapping
from ...types import LineNumberRange

class ContextMappingGenerationState(BaseModelWithItem):
    """단일 Context Mapping 생성 처리 상태"""
    requirements: str = ""
    line_numbered_requirements: str = ""
    boundedContexts: List[BoundedContextInfoModel] = Field(default_factory=list)
    worker_index: int = 0

    created_context_mappings: List[ContextMapping] = Field(default_factory=list)

    retry_count: int = 0
    generation_complete: bool = False
    is_preprocess_completed: bool = False
    is_failed: bool = False

class CreateContextMappingModel(BaseModelWithItem):
    """Context Mapping 생성 관련 상태 관리 모델"""
    worker_generations: Dict[str, ContextMappingGenerationState] = Field(default_factory=dict)
    
    current_batch: List[ContextMappingGenerationState] = Field(default_factory=list)
    parallel_worker_results: List[ContextMappingGenerationState] = Field(default_factory=list)
    
    completed_generations: List[ContextMappingGenerationState] = Field(default_factory=list)
    pending_generations: List[ContextMappingGenerationState] = Field(default_factory=list)
    
    is_processing: bool = False
    all_complete: bool = False
    is_merge_completed: bool = False
    
    max_retry_count: int = 3
    is_failed: bool = False

    total_seconds: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0

    accumulated_line_number_ranges: Dict[str, List[LineNumberRange]] = Field(default_factory=dict)