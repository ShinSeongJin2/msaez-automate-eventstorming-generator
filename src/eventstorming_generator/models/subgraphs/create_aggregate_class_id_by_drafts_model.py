from typing import Dict, Any, List, Optional

from ..base import BaseModelWithItem
from ..action_model import ActionModel

class ClassIdGenerationState(BaseModelWithItem):
    """단일 Aggregate 클래스 ID 생성 처리 상태"""
    target_references: List[str] = []
    draft_option: Dict[str, Any] = {}
    summarized_es_value: Dict[str, Any] = {}
    created_actions: List[ActionModel] = []
    retry_count: int = 0
    generation_complete: bool = False
    is_token_over_limit: bool = False

class CreateAggregateClassIdByDraftsModel(BaseModelWithItem):
    """Aggregate 클래스 ID 생성 관련 상태 관리 모델"""
    # 처리할 초안 및 참조 목록
    draft_options: Dict[str, Any] = {}
    
    # 현재 처리 중인 클래스 ID 생성 상태
    current_generation: Optional[ClassIdGenerationState] = None
    
    # 처리 완료된 클래스 ID 생성 목록
    completed_generations: List[ClassIdGenerationState] = []
    
    # 처리 대기 중인 클래스 ID 생성 목록
    pending_generations: List[ClassIdGenerationState] = []
    
    # 전체 진행 상태
    is_processing: bool = False
    all_complete: bool = False
    
    # 최대 재시도 횟수
    max_retry_count: int = 3
    
    # 최종적으로 실행 실패 여부
    is_failed: bool = False