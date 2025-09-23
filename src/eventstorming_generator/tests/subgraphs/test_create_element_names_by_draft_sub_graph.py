from ..mocks import create_element_names_by_draft_sub_graph_inputs
from ...subgraphs import create_element_names_by_draft_sub_graph
from ..test_utils import TestUtils
from ...utils import LoggingUtil

def test_create_element_names_by_draft_sub_graph():
    try:

        run_subgraph = create_element_names_by_draft_sub_graph()
        result = run_subgraph(create_element_names_by_draft_sub_graph_inputs)
        TestUtils.save_dict_to_temp_file({
            "extracted_element_names": result.subgraphs.createElementNamesByDraftsModel.extracted_element_names,
            "totalSeconds": result.subgraphs.createElementNamesByDraftsModel.total_seconds
        }, "test_create_element_names_by_draft_sub_graph")
        
    except Exception as e:
        LoggingUtil.exception("test_create_element_names_by_draft_sub_graph", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_create_element_names_by_draft_sub_graph_error")
        raise
