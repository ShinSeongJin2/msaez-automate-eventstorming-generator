from ...mocks import gwt_worker_subgraph_inputs
from ....subgraphs import create_gwt_worker_subgraph, gwt_worker_id_context
from ...test_utils import TestUtils
from ....utils import LoggingUtil

def test_gwt_worker_sub_graph():
    try:

        worker_id = 'dc95ecbe-b66a-4fad-91a3-71dd351ddcaf'

        run_subgraph = create_gwt_worker_subgraph()
        gwt_worker_id_context.set(worker_id)
        result = run_subgraph(gwt_worker_subgraph_inputs)

        completed_gwt = result.subgraphs.createGwtGeneratorByFunctionModel.worker_generations.get(worker_id)

        TestUtils.save_dict_to_temp_file(completed_gwt, "completed_gwt")
        TestUtils.save_dict_to_temp_file({
            "elements": [completed_gwt.command_to_replace],
            "relations": []
        }, "completed_value")

    except Exception as e:
        LoggingUtil.exception("test_gwt_worker_sub_graph", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_gwt_worker_sub_graph_error")
        raise
