from typing import Dict, Any, List
from pydantic import Field

from ..base import BaseModelWithItem

class GWTGenerationState(BaseModelWithItem):
    """단일 Command의 GWT 생성 처리 상태"""
    target_bounded_context: Dict[str, Any] = Field(default_factory=dict)
    target_command_id: str = ""
    target_aggregate_name: str = ""
    description: str = ""
    summarized_es_value: Dict[str, Any] = Field(default_factory=dict)
    target_command_alias: str = ""
    retry_count: int = 0
    command_to_replace: Dict[str, Any] = Field(default_factory=dict)
    generation_complete: bool = False
    is_token_over_limit: bool = False
    
    needs_es_summary: bool = False
    es_summary_context: str = ""
    es_summary_max_tokens: int = 0
    es_summary_processing: bool = False
    es_summary_complete: bool = False

class CreateGwtGeneratorByFunctionModel(BaseModelWithItem):
    """GWT 생성 관련 상태 관리 모델"""
    draft_options: Dict[str, Any] = Field(default_factory=dict)
    
    completed_generations: List[GWTGenerationState] = Field(default_factory=list)
    pending_generations: List[GWTGenerationState] = Field(default_factory=list)
    
    worker_generations: Dict[str, GWTGenerationState] = Field(default_factory=dict)
    current_batch: List[GWTGenerationState] = Field(default_factory=list)
    parallel_worker_results: List[GWTGenerationState] = Field(default_factory=list)
    
    is_processing: bool = False
    all_complete: bool = False
    
    max_retry_count: int = 3
    is_failed: bool = False

    total_seconds: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0