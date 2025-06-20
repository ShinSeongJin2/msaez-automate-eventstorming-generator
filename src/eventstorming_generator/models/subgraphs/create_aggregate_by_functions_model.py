from typing import Dict, Any, List, Optional

from ..base import BaseModelWithItem
from ..action_model import ActionModel

class AggregateGenerationState(BaseModelWithItem):
    """단일 Aggregate 생성 처리 상태"""
    target_bounded_context: Dict[str, Any] = {}
    target_aggregate: Dict[str, Any] = {}
    description: str = ""
    draft_option: List[Dict[str, Any]] = []
    summarized_es_value: Dict[str, Any] = {}
    is_accumulated: bool = False
    retry_count: int = 0
    created_actions: List[ActionModel] = []
    generation_complete: bool = False
    is_token_over_limit: bool = False

class CreateAggregateByFunctionsModel(BaseModelWithItem):
    """Aggregate 생성 관련 상태 관리 모델"""
    # 현재 처리 중인 Aggregate 상태
    current_generation: Optional[AggregateGenerationState] = None
    
    # 처리 완료된 Aggregate 목록
    completed_generations: List[AggregateGenerationState] = []
    
    # 처리 대기 중인 Aggregate 목록
    pending_generations: List[AggregateGenerationState] = []
    
    # 전체 진행 상태
    is_processing: bool = False
    all_complete: bool = False
    
    # 최대 재시도 횟수
    max_retry_count: int = 3

    # 최종적으로 실행 실패 여부
    is_failed: bool = False
