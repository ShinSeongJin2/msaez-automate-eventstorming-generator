import os

from ..test_utils import TestUtils
from ...generators import SanityCheckGenerator
from ...utils import LoggingUtil

def test_sanity_check_generator():
    try:

        result = SanityCheckGenerator(os.getenv("AI_MODEL"), {}, {
            "inputs": {
                "text": "Hello, World !"
            }
        }).generate()
        TestUtils.save_dict_to_temp_file(result, "test_sanity_check_generator")

    except Exception as e:
        LoggingUtil.exception("test_sanity_check_generator", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_sanity_check_generator_error")
        raise
