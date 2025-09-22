from ...mocks import class_id_worker_subgraph_inputs
from ....subgraphs import create_class_id_worker_subgraph, class_id_worker_id_context
from ...test_utils import TestUtils
from ....utils import LoggingUtil

def test_class_id_worker_subgraph():
    try:

        worker_id = '9439b794-f494-4755-93d1-7035b10c7f64'

        run_subgraph = create_class_id_worker_subgraph()
        class_id_worker_id_context.set(worker_id)
        result = run_subgraph(class_id_worker_subgraph_inputs)

        completed_class_id = result.subgraphs.createAggregateClassIdByDraftsModel.worker_generations.get(worker_id)

        TestUtils.save_dict_to_temp_file(completed_class_id, "completed_class_id")
        TestUtils.save_dict_to_temp_file({
            "created_actions": completed_class_id.created_actions,
        }, "completed_created_actions")

    except Exception as e:
        LoggingUtil.exception("test_class_id_worker_subgraph", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_class_id_worker_subgraph_error")
        raise
