import os
import time
from datetime import datetime
from typing import Any

from ..generators import XmlBaseGenerator
from ..utils import EsAliasTransManager, ESValueSummarizeWithFilter, JsonUtil, LoggingUtil
from ..config import Config

class TestUtils:
    @staticmethod
    def save_dict_to_temp_file(data: Any, file_name: str) -> None:
        os.makedirs(".temp", exist_ok=True)

        json_data = JsonUtil.convert_to_json(data)  
        print(json_data)
        
        TIME = datetime.now().strftime('%Y%m%d_%H%M%S')
        FILE_PATH = f".temp/{TIME}_{file_name}.json"
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            f.write(json_data)
        print(f"{FILE_PATH} 파일에 생성 결과 저장 완료")
    
    @staticmethod
    def save_es_summarize_result_to_temp_file(es_value: Any, file_name: str) -> None:
        es_alias_trans_manager = EsAliasTransManager(es_value)
        summarized_es_value = ESValueSummarizeWithFilter.get_summarized_es_value(es_value, [], es_alias_trans_manager)
        TestUtils.save_dict_to_temp_file(summarized_es_value, f"{file_name}_es_value_summarized")

    @staticmethod
    def test_generator(generator: XmlBaseGenerator, inputs: dict, model_type: str = "normal") -> dict:
        try:

            model_name = Config.get_ai_model()
            if model_type == "light":
                model_name = Config.get_ai_model_light()

            generator = generator(model_name, {}, {
                "preferredLanguage": "Korean",
                "inputs": inputs
            })
            entire_prompt = generator.get_entire_prompt()

            start_time = time.time()
            result = generator.generate()
            end_time = time.time()
            total_seconds = end_time - start_time

            result["total_seconds"] = total_seconds

            TestUtils.save_dict_to_temp_file(entire_prompt, f"test_input_{generator.__class__.__name__}")
            TestUtils.save_dict_to_temp_file(result, f"test_output_{generator.__class__.__name__}")

        except Exception as e:
            LoggingUtil.exception(f"test_error_{generator.__class__.__name__}", f"테스트 실패", e)
            TestUtils.save_dict_to_temp_file({
                "error": str(e)
            }, f"test_error_{generator.__class__.__name__}")
            raise