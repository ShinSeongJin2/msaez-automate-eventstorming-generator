from datetime import datetime
from typing import Any

from ..utils import EsAliasTransManager, ESValueSummarizeWithFilter, JsonUtil

class TestUtils:
    @staticmethod
    def save_dict_to_temp_file(data: Any, file_name: str) -> None:
        json_data = JsonUtil.convert_to_json(data)  
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
