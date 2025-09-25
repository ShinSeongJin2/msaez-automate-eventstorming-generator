from ...mocks import policy_actions_worker_subgraph_inputs
from ....subgraphs import create_policy_actions_worker_subgraph, policy_actions_worker_id_context
from ...run_util import RunUtil
from ....utils import LoggingUtil
from ....models import State

def run_policy_actions_worker_subgraph():
    run_name = "run_policy_actions_worker_subgraph"

    try:

        worker_id = '62795ea6-bcbb-443b-88ac-39c0c9255be1'

        run_subgraph = create_policy_actions_worker_subgraph()
        policy_actions_worker_id_context.set(worker_id)
        result: State = run_subgraph(policy_actions_worker_subgraph_inputs)

        completed_policy_actions = result.subgraphs.createPolicyActionsByFunctionModel.worker_generations.get(worker_id)

        RunUtil.save_dict_to_temp_file(completed_policy_actions, f"{run_name}_completed_policy_actions")
        RunUtil.save_dict_to_temp_file({
            "extractedPolicies": [completed_policy_actions.extractedPolicies],
            "logs": result.outputs.logs,
        }, f"{run_name}_extractedPolicies")
        RunUtil.check_error_logs_from_state(result, run_name)

    except Exception as e:
        LoggingUtil.exception(run_name, f"실행 실패", e)
        RunUtil.save_dict_to_temp_file({
            "error": str(e)
        }, f"{run_name}_error")
        raise
