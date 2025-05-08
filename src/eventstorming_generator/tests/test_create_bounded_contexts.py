from .mocks import input_state
from ..graph import create_bounded_contexts

def test_create_bounded_contexts():
    result = create_bounded_contexts(input_state)
    print(result)