from ..test_utils import TestUtils
from ...generators import ESValueSummaryGenerator
from ..mocks import es_value_summary_generator_inputs
import os

def test_es_value_summary_generator():
    try:

        result = ESValueSummaryGenerator(os.getenv("AI_MODEL"), {}, {
            "preferredLanguage": "Korean",
            "inputs": {
                "context": es_value_summary_generator_inputs["context"],
                "elementIds": es_value_summary_generator_inputs["elementIds"]
            }
        }).generate()
        TestUtils.save_dict_to_temp_file(result, "test_es_value_summary_generator")

    except Exception as e:
        print(f"테스트 실패: {str(e)}")
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_es_value_summary_generator_error")
        raise
