from ...mocks import policy_actions_worker_subgraph_inputs
from ....subgraphs import create_policy_actions_worker_subgraph, policy_actions_worker_id_context
from ...test_utils import TestUtils
from ....utils import LoggingUtil

def test_policy_actions_worker_subgraph():
    try:

        worker_id = '62795ea6-bcbb-443b-88ac-39c0c9255be1'

        run_subgraph = create_policy_actions_worker_subgraph()
        policy_actions_worker_id_context.set(worker_id)
        result = run_subgraph(policy_actions_worker_subgraph_inputs)

        completed_policy_actions = result.subgraphs.createPolicyActionsByFunctionModel.worker_generations.get(worker_id)

        TestUtils.save_dict_to_temp_file(completed_policy_actions, "completed_policy_actions")
        TestUtils.save_dict_to_temp_file({
            "extractedPolicies": [completed_policy_actions.extractedPolicies],
        }, "completed_extractedPolicies")

    except Exception as e:
        LoggingUtil.exception("test_policy_actions_worker_subgraph", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_policy_actions_worker_subgraph_error")
        raise
