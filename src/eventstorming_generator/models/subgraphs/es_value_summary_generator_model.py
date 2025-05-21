from typing import Dict, Any, List, Optional
from pydantic import BaseModel

class ESValueSummaryGeneratorModel(BaseModel):
    """ES 값 요약 생성 관련 상태 관리 모델"""
    
    # 요약 작업 상태
    is_processing: bool = False
    is_complete: bool = False
    is_failed: bool = False
    
    # 요약 입력 데이터
    context: str = ""
    es_value: Dict[str, Any] = {}
    keys_to_filter: List[str] = []
    max_tokens: int = 0
    token_calc_model_vendor: str = ""
    token_calc_model_name: str = ""
    
    # 요약 작업 결과
    summarized_es_value: Dict[str, Any] = {}
    processed_summarized_es_value: Dict[str, Any] = {}
    element_ids: List[str] = []
    sorted_element_ids: List[str] = []
    
    # 작업 흐름 제어
    retry_count: int = 0
    max_retry_count: int = 3