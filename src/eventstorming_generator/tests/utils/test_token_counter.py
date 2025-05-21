from ...utils import TokenCounter
from ..test_utils import TestUtils

def test_token_counter():
    try:

        token_count = TokenCounter.get_token_count("Hello, world!", "openai", "gpt-4.1-2025-04-14")
        print(token_count)

    except Exception as e:
        print(f"테스트 실패: {str(e)}")
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_token_counter")
        raise