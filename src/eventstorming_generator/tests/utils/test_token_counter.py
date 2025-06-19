from ...utils import TokenCounter
from ..test_utils import TestUtils
from ...utils import LoggingUtil

def test_token_counter():
    try:

        token_count = TokenCounter.get_token_count("Hello, world!", "openai", "gpt-4.1-2025-04-14")
        LoggingUtil.info("test_token_counter", f"토큰 수: {token_count}")

    except Exception as e:
        LoggingUtil.exception("test_token_counter", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_token_counter")
        raise