from typing import Dict, Any, List, Optional

from ..base import BaseModelWithItem
from ..action_model import ActionModel

class GWTGenerationState(BaseModelWithItem):
    """단일 Command의 GWT 생성 처리 상태"""
    target_bounded_context: Dict[str, Any] = {}
    target_command_ids: List[str] = []
    target_aggregate_names: List[str] = []
    description: str = ""
    summarized_es_value: Dict[str, Any] = {}
    es_alias_trans_manager: Any = None
    target_command_aliases: List[str] = []
    retry_count: int = 0
    commands_to_replace: List[Dict[str, Any]] = []
    generation_complete: bool = False

class CreateGwtGeneratorByFunctionModel(BaseModelWithItem):
    """GWT 생성 관련 상태 관리 모델"""
    # 처리할 초안 목록
    draft_options: Dict[str, Any] = {}
    
    # 현재 처리 중인 GWT 생성 상태
    current_generation: Optional[GWTGenerationState] = None
    
    # 처리 완료된 GWT 생성 목록
    completed_generations: List[GWTGenerationState] = []
    
    # 처리 대기 중인 GWT 생성 목록
    pending_generations: List[GWTGenerationState] = []
    
    # 전체 진행 상태
    is_processing: bool = False
    all_complete: bool = False
    
    # 최대 재시도 횟수
    max_retry_count: int = 3

    # 최종적으로 실행 실패 여부
    is_failed: bool = False