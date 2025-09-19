from typing import Dict, Any, List, Optional
from pydantic import Field

from ..base import BaseModelWithItem
from ..action_model import ActionModel

class PolicyActionGenerationState(BaseModelWithItem):
    """단일 Policy 액션 생성 처리 상태"""
    target_bounded_context: Dict[str, Any] = Field(default_factory=dict)
    description: str = ""
    original_description: str = ""
    summarized_es_value: Dict[str, Any] = Field(default_factory=dict)
    is_accumulated: bool = False
    retry_count: int = 0
    created_actions: List[ActionModel] = Field(default_factory=list)
    generation_complete: bool = False
    subject_text: str = ""
    is_token_over_limit: bool = False

class CreatePolicyActionsByFunctionModel(BaseModelWithItem):
    """Policy 액션 생성 관련 상태 관리 모델"""
    draft_options: Dict[str, Any] = Field(default_factory=dict)
    current_generation: Optional[PolicyActionGenerationState] = None
    completed_generations: List[PolicyActionGenerationState] = Field(default_factory=list)
    pending_generations: List[PolicyActionGenerationState] = Field(default_factory=list)
    
    is_processing: bool = False
    all_complete: bool = False
    
    max_retry_count: int = 3
    is_failed: bool = False

    total_seconds: float = 0.0
    start_time: float = 0.0
    end_time: float = 0.0