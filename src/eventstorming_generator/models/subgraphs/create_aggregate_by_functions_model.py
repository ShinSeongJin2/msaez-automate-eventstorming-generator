from typing import Dict, Any, List, Optional
from pydantic import Field

from ..base import BaseModelWithItem
from ..action_model import ActionModel

class AggregateGenerationState(BaseModelWithItem):
    """단일 Aggregate 생성 처리 상태"""
    target_bounded_context: Dict[str, Any] = Field(default_factory=dict)
    target_aggregate: Dict[str, Any] = Field(default_factory=dict)
    description: str = ""
    original_description: str = ""
    requirements: Dict[str, Any] = Field(default_factory=dict)
    draft_option: List[Dict[str, Any]] = Field(default_factory=list)
    summarized_es_value: Dict[str, Any] = Field(default_factory=dict)
    is_accumulated: bool = False
    retry_count: int = 0
    created_actions: List[ActionModel] = Field(default_factory=list)
    generation_complete: bool = False
    is_token_over_limit: bool = False
    extracted_ddl_fields: List[str] = Field(default_factory=list)
    missing_ddl_fields: List[str] = Field(default_factory=list)
    ddl_extraction_attempted: bool = False
    ddl_fields: List[str] = Field(default_factory=list)  # 애그리거트별로 할당된 DDL 필드 목록
    is_action_postprocess_completed: bool = False

class CreateAggregateByFunctionsModel(BaseModelWithItem):
    """Aggregate 생성 관련 상태 관리 모델"""
    # 현재 처리 중인 Aggregate 상태
    current_generation: Optional[AggregateGenerationState] = None
    
    # 처리 완료된 Aggregate 목록
    completed_generations: List[AggregateGenerationState] = Field(default_factory=list)
    
    # 처리 대기 중인 Aggregate 목록
    pending_generations: List[AggregateGenerationState] = Field(default_factory=list)
    
    # 전체 진행 상태
    is_processing: bool = False
    all_complete: bool = False
    
    # 최대 재시도 횟수
    max_retry_count: int = 3

    # 최종적으로 실행 실패 여부
    is_failed: bool = False
    
    # DDL 처리 관련 상태
    ddl_extraction_complete: bool = False
    ddl_assignment_complete: bool = False
    all_ddl_fields: List[str] = Field(default_factory=list)  # BC에서 추출된 전체 DDL 필드
