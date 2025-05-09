import json
from datetime import datetime
from typing import Any

from ..utils import EsAliasTransManager, ESValueSummarizeWithFilter

class TestUtils:
    @staticmethod
    def save_dict_to_temp_file(data: Any, file_name: str) -> None:
        # 데이터 변환 함수
        def convert_data(item):
            if hasattr(item, 'model_dump_json'):
                return json.loads(item.model_dump_json())
            elif isinstance(item, dict):
                return item
            else:
                return str(item)
        
        # 리스트인 경우 각 항목을 개별적으로 처리
        if isinstance(data, list):
            processed_data = [convert_data(item) for item in data]
            json_data = json.dumps(processed_data, indent=4, ensure_ascii=False)
        # Pydantic BaseModel인 경우
        elif hasattr(data, 'model_dump_json'):
            json_data = data.model_dump_json(indent=4)
        # 딕셔너리인 경우
        elif isinstance(data, dict):
            json_data = json.dumps(data, indent=4, ensure_ascii=False)
        # 그 외의 경우
        else:
            json_data = str(data)
        
        print(json_data)
        
        TIME = datetime.now().strftime('%Y%m%d_%H%M%S')
        FILE_PATH = f".temp/{TIME}_{file_name}.json"
        with open(FILE_PATH, "w") as f:
            f.write(json_data)
        print(f"{FILE_PATH} 파일에 생성 결과 저장 완료")
    
    @staticmethod
    def save_es_summarize_result_to_temp_file(es_value: Any, file_name: str) -> None:
        es_alias_trans_manager = EsAliasTransManager(es_value)
        summarized_es_value = ESValueSummarizeWithFilter.get_summarized_es_value(es_value, [], es_alias_trans_manager)
        TestUtils.save_dict_to_temp_file(summarized_es_value, f"{file_name}_es_value_summarized")
