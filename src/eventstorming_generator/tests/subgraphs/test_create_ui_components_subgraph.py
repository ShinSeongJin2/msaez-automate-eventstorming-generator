from ..mocks import create_ui_components_subgraph_inputs
from ...subgraphs import create_ui_components_subgraph
from ..test_utils import TestUtils
from ...utils import LoggingUtil

def test_create_ui_components_subgraph():
    try:

        run_subgraph = create_ui_components_subgraph()
        result = run_subgraph(create_ui_components_subgraph_inputs)
        TestUtils.save_dict_to_temp_file(result.outputs.esValue, "test_create_ui_components_subgraph")
        TestUtils.save_es_summarize_result_to_temp_file(result.outputs.esValue, "test_create_ui_components_subgraph")
        
    except Exception as e:
        LoggingUtil.exception("test_create_ui_components_subgraph", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_create_ui_components_subgraph")
        raise
