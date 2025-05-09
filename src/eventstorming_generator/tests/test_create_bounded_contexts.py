from .mocks import input_state
from ..graph import create_bounded_contexts
from .save_to_temp_file import save_to_temp_file

def test_create_bounded_contexts():
    try:
        result = create_bounded_contexts(input_state)
        save_to_temp_file(result, "test_create_bounded_contexts")
    except Exception as e:
        print(f"테스트 실패: {str(e)}")
        raise
