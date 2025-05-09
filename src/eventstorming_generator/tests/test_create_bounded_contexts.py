from .mocks import input_state
from ..graph import create_bounded_contexts
from .test_utils import TestUtils

def test_create_bounded_contexts():
    try:

        result = create_bounded_contexts(input_state)
        TestUtils.save_dict_to_temp_file(result, "test_create_bounded_contexts")
        TestUtils.save_es_summarize_result_to_temp_file(result.outputs.esValue, "test_create_bounded_contexts")

    except Exception as e:
        print(f"테스트 실패: {str(e)}")
        TestUtils.save_dict_to_temp_file({
            "error": str(e),
            "input_state": input_state
        }, "test_create_bounded_contexts_error")
        raise
