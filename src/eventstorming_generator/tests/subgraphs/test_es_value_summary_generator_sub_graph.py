from ..mocks import es_value_summary_generator_sub_graph_inputs
from ...subgraphs import create_es_value_summary_generator_subgraph
from ..test_utils import TestUtils
from ...utils import LoggingUtil

def test_es_value_summary_generator_sub_graph():
    try:

        run_subgraph = create_es_value_summary_generator_subgraph()
        result = run_subgraph(es_value_summary_generator_sub_graph_inputs)
        TestUtils.save_dict_to_temp_file(result.subgraphs.esValueSummaryGeneratorModel, "test_es_value_summary_generator_sub_graph")
        
    except Exception as e:
        LoggingUtil.exception("test_es_value_summary_generator_sub_graph", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_es_value_summary_generator_sub_graph")
        raise
