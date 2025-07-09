import os

from ..test_utils import TestUtils
from ...generators import ExtractDDLFieldsGenerator
from ..mocks import extract_ddl_fields_generator_inputs
from ...utils import LoggingUtil

def test_extract_ddl_fields_generator():
    try:

        result = ExtractDDLFieldsGenerator(os.getenv("AI_MODEL"), {}, {
            "preferredLanguage": "Korean",
            "inputs": {
                "ddl": extract_ddl_fields_generator_inputs["ddl"]
            }
        }).generate()
        TestUtils.save_dict_to_temp_file(result, "test_extract_ddl_fields_generator")

    except Exception as e:
        LoggingUtil.exception("test_extract_ddl_fields_generator", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_extract_ddl_fields_generator_error")
        raise
