from typing import Dict, Any, List
from pydantic import Field

from ..base import BaseModelWithItem

class PolicyActionGenerationState(BaseModelWithItem):
    """단일 Policy 액션 생성 처리 상태"""
    target_bounded_context: Dict[str, Any] = Field(default_factory=dict)
    description: str = ""
    original_description: str = ""
    summarized_es_value: Dict[str, Any] = Field(default_factory=dict)

    retry_count: int = 0
    extractedPolicies: List[Any] = Field(default_factory=list)
    
    generation_complete: bool = False
    is_token_over_limit: bool = False
    is_failed: bool = False

class CreatePolicyActionsByFunctionModel(BaseModelWithItem):
    """Policy 액션 생성 관련 상태 관리 모델"""
    draft_options: Dict[str, Any] = Field(default_factory=dict)
    
    completed_generations: List[PolicyActionGenerationState] = Field(default_factory=list)
    pending_generations: List[PolicyActionGenerationState] = Field(default_factory=list)
    
    worker_generations: Dict[str, PolicyActionGenerationState] = Field(default_factory=dict)
    current_batch: List[PolicyActionGenerationState] = Field(default_factory=list)
    parallel_worker_results: List[PolicyActionGenerationState] = Field(default_factory=list)
    
    created_policy_relations: List[str] = Field(default_factory=list)
    
    is_processing: bool = False
    all_complete: bool = False
    
    max_retry_count: int = 3
    is_failed: bool = False

    total_seconds: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0