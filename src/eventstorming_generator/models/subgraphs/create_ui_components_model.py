from typing import List, Optional, Dict, Any

from ..base import BaseModelWithItem
from ..action_model import ActionModel

class CreateUiComponentsGenerationState(BaseModelWithItem):
    """단일 UIComponents 생성 처리 상태"""
    target_ui_component: Dict[str, Any] = {}
    ai_request_type: str = ""
    ai_input_data: Dict[str, Any] = {}
    related_site_map_object: Dict[str, Any] = {}
    ui_replace_actions: List[ActionModel] = []
    retry_count: int = 0
    generation_complete: bool = False
    is_failed: bool = False

class CreateUiComponentsModel(BaseModelWithItem):
    """UIComponents 생성 관련 상태 관리 모델"""
    # 현재 처리 중인 UIComponents 생성 상태
    current_generation: Optional[CreateUiComponentsGenerationState] = None
    
    # 처리 완료된 UIComponents 생성 목록
    completed_generations: List[CreateUiComponentsGenerationState] = []
    
    # 처리 대기 중인 UIComponents 생성 목록
    pending_generations: List[CreateUiComponentsGenerationState] = []
    
    # 전체 진행 상태
    is_processing: bool = False
    all_complete: bool = False
    
    # 최대 재시도 횟수
    max_retry_count: int = 3

    # 최종적으로 실행 실패 여부
    is_failed: bool = False