from ...mocks import aggregate_worker_subgraph_inputs
from ....subgraphs import create_aggregate_worker_subgraph, aggregate_worker_id_context
from ...run_util import RunUtil
from ....utils import LoggingUtil
from ....models import State

def run_aggregate_worker_subgraph():
    run_name = "run_aggregate_worker_subgraph"

    try:

        worker_id = '6799ce3e-f2ec-48cb-b4f1-91e8316eab91'

        run_subgraph = create_aggregate_worker_subgraph()
        aggregate_worker_id_context.set(worker_id)
        result: State = run_subgraph(aggregate_worker_subgraph_inputs)

        completed_aggregate = result.subgraphs.createAggregateByFunctionsModel.worker_generations.get(worker_id)

        RunUtil.save_dict_to_temp_file(completed_aggregate, f"{run_name}_completed_aggregate")
        RunUtil.save_dict_to_temp_file({
            "created_actions": completed_aggregate.created_actions,
            "logs": result.outputs.logs,
        }, f"{run_name}_created_actions")
        RunUtil.check_error_logs_from_state(result, run_name)

    except Exception as e:
        LoggingUtil.exception(run_name, f"실행 실패", e)
        RunUtil.save_dict_to_temp_file({
            "error": str(e)
        }, f"{run_name}_error")
        raise
