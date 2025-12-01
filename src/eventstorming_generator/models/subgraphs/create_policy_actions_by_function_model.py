from typing import Dict, Any, List, Optional
from pydantic import Field

from ..base import BaseModelWithItem
from ...types import RequirementIndexMapping

class PolicyActionGenerationState(BaseModelWithItem):
    """단일 Policy 액션 생성 처리 상태"""
    target_bounded_context_name: str = Field(default_factory=str)
    description: str = ""
    original_description: str = ""
    requirement_index_mapping: Optional[RequirementIndexMapping] = None
    worker_index: int = 0

    summarized_es_value: Dict[str, Any] = Field(default_factory=dict)
    extractedPolicies: List[Any] = Field(default_factory=list)

    retry_count: int = 0    
    generation_complete: bool = False
    is_token_over_limit: bool = False
    is_failed: bool = False

class CreatePolicyActionsByFunctionModel(BaseModelWithItem):
    """Policy 액션 생성 관련 상태 관리 모델"""
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