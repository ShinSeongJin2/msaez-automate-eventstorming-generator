from ..mocks import create_command_actions_by_function_sub_graph_inputs
from ...subgraphs import create_command_actions_by_function_subgraph
from ..test_utils import TestUtils

def test_create_command_actions_by_function_sub_graph():
    try:

        run_subgraph = create_command_actions_by_function_subgraph()
        result = run_subgraph(create_command_actions_by_function_sub_graph_inputs)
        TestUtils.save_dict_to_temp_file(result.outputs.esValue, "test_create_command_actions_by_function_sub_graph")
        TestUtils.save_es_summarize_result_to_temp_file(result.outputs.esValue, "test_create_command_actions_by_function_sub_graph")
        
    except Exception as e:
        print(f"테스트 실패: {str(e)}")
        TestUtils.save_dict_to_temp_file({
            "error": str(e),
            "input_state": create_command_actions_by_function_sub_graph_inputs
        }, "test_create_command_actions_by_function_sub_graph_error")
        raise
