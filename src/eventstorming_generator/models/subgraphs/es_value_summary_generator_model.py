from typing import Dict, Any, List
from pydantic import Field

from ..base import BaseModelWithItem

class ESValueSummaryGeneratorModel(BaseModelWithItem):
    """ES 값 요약 생성 관련 상태 관리 모델"""
    
    # 요약 작업 상태
    is_processing: bool = False
    is_complete: bool = False
    is_failed: bool = False
    
    # 요약 입력 데이터
    context: str = ""
    keys_to_filter: List[str] = Field(default_factory=list)
    max_tokens: int = 0
    token_calc_model_vendor: str = ""
    token_calc_model_name: str = ""
    
    # 요약 작업 결과
    summarized_es_value: Dict[str, Any] = Field(default_factory=dict)
    processed_summarized_es_value: Dict[str, Any] = Field(default_factory=dict)
    element_ids: List[str] = Field(default_factory=list)
    sorted_element_ids: List[str] = Field(default_factory=list)
    
    # 작업 흐름 제어
    retry_count: int = 0
    max_retry_count: int = 3

    # 요약된 데이터 형태
    is_xml_format: bool = False