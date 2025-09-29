import os
import time
from datetime import datetime
from typing import Any

from ..generators import XmlBaseGenerator
from ..utils import EsAliasTransManager, ESValueSummarizeWithFilter, JsonUtil, LoggingUtil
from ..config import Config
from ..models import State

class RunUtil:
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
        RunUtil.save_dict_to_temp_file(summarized_es_value, f"{file_name}_es_value_summarized")

    @staticmethod
    def check_error_logs_from_state(state: State, file_name: str) -> None:
        logs_to_check = state.outputs.logs

        error_logs = []
        for log in logs_to_check:
            if log.level == "error":
                error_logs.append(log)
        
        if len(error_logs) > 0:
            print(f"[!] Error logs found: {error_logs}")
            RunUtil.save_dict_to_temp_file(error_logs, f"{file_name}_error_logs")
        else:
            print(f"[*] No error logs found")        

    @staticmethod
    def run_generator(generator: XmlBaseGenerator, inputs: dict, model_type: str = "normal") -> dict:
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
            generator_output = generator.generate()
            end_time = time.time()
            total_seconds = end_time - start_time

            generator_output["result"] = generator_output["result"].model_dump()
            generator_output["total_seconds"] = total_seconds

            RunUtil.save_dict_to_temp_file(entire_prompt, f"run_input_{generator.__class__.__name__}")
            RunUtil.save_dict_to_temp_file(generator_output, f"run_output_{generator.__class__.__name__}")

        except Exception as e:
            LoggingUtil.exception(f"run_error_{generator.__class__.__name__}", f"실행 실패", e)
            RunUtil.save_dict_to_temp_file({
                "error": str(e)
            }, f"run_error_{generator.__class__.__name__}")
            raise