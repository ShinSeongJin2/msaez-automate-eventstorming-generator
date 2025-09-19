from ...mocks import aggregate_worker_subgraph_inputs
from ....subgraphs import create_aggregate_worker_subgraph, aggregate_worker_id_context
from ...test_utils import TestUtils
from ....utils import LoggingUtil

def test_aggregate_worker_subgraph():
    try:

        worker_id = '6799ce3e-f2ec-48cb-b4f1-91e8316eab91'

        run_subgraph = create_aggregate_worker_subgraph()
        aggregate_worker_id_context.set(worker_id)
        result = run_subgraph(aggregate_worker_subgraph_inputs)

        completed_aggregate = result.subgraphs.createAggregateByFunctionsModel.worker_generations.get(worker_id)

        TestUtils.save_dict_to_temp_file(completed_aggregate, "completed_aggregate")
        TestUtils.save_dict_to_temp_file({
            "created_actions": completed_aggregate.created_actions,
        }, "completed_created_actions")

    except Exception as e:
        LoggingUtil.exception("test_aggregate_worker_subgraph", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_aggregate_worker_subgraph_error")
        raise
