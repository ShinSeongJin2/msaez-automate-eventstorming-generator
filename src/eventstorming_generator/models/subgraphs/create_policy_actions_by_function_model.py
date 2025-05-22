from typing import Dict, Any, List, Optional

from ..base import BaseModelWithItem
from ..action_model import ActionModel

class PolicyActionGenerationState(BaseModelWithItem):
    """단일 Policy 액션 생성 처리 상태"""
    target_bounded_context: Dict[str, Any] = {}
    description: str = ""
    summarized_es_value: Dict[str, Any] = {}
    es_alias_trans_manager: Optional[Any] = None
    is_accumulated: bool = False
    retry_count: int = 0
    created_actions: List[ActionModel] = []
    generation_complete: bool = False
    subject_text: str = ""
    is_token_over_limit: bool = False

class CreatePolicyActionsByFunctionModel(BaseModelWithItem):
    """Policy 액션 생성 관련 상태 관리 모델"""
    # 처리할 초안 목록
    draft_options: Dict[str, Any] = {}
    
    # 현재 처리 중인 Policy 액션 생성 상태
    current_generation: Optional[PolicyActionGenerationState] = None
    
    # 처리 완료된 Policy 액션 목록
    completed_generations: List[PolicyActionGenerationState] = []
    
    # 처리 대기 중인 Policy 액션 목록
    pending_generations: List[PolicyActionGenerationState] = []
    
    # 전체 진행 상태
    is_processing: bool = False
    all_complete: bool = False
    
    # 최대 재시도 횟수
    max_retry_count: int = 3

    # 최종적으로 실행 실패 여부
    is_failed: bool = False