from eventstorming_generator.models.state import State
from .mocks import input_state
from ..graph import graph
from .test_utils import TestUtils

def test_graph():
    try:
        
        result = State(**graph.invoke(input_state))
        TestUtils.save_dict_to_temp_file(result, "test_graph")
        TestUtils.save_es_summarize_result_to_temp_file(result.outputs.esValue, "test_graph")

    except Exception as e:
        print(f"테스트 실패: {str(e)}")
        TestUtils.save_dict_to_temp_file({
            "error": str(e),
            "input_state": input_state
        }, "test_graph_error")
        raise
