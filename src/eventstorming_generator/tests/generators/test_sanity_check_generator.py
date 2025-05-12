from ..test_utils import TestUtils
from ...generators import SanityCheckGenerator
import os

def test_sanity_check_generator():
    try:

        result = SanityCheckGenerator(os.getenv("AI_MODEL"), {}, {
            "inputs": {
                "text": "Hello, World !"
            }
        }).generate()
        TestUtils.save_dict_to_temp_file(result, "test_sanity_check_generator")

    except Exception as e:
        print(f"테스트 실패: {str(e)}")
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_sanity_check_generator_error")
        raise
