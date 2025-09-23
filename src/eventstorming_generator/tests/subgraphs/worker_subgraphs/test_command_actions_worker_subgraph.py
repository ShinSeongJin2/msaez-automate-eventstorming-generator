from ...mocks import command_actions_worker_subgraph_inputs
from ....subgraphs import create_command_actions_worker_subgraph, command_actions_worker_id_context
from ...test_utils import TestUtils
from ....utils import LoggingUtil

def test_command_actions_worker_subgraph():
    try:

        worker_id = 'bd0ee73e-e6cb-46a4-b8c7-4f9c8865558e'

        run_subgraph = create_command_actions_worker_subgraph()
        command_actions_worker_id_context.set(worker_id)
        result = run_subgraph(command_actions_worker_subgraph_inputs)

        completed_command_actions = result.subgraphs.createCommandActionsByFunctionModel.worker_generations.get(worker_id)

        TestUtils.save_dict_to_temp_file(completed_command_actions, "completed_command_actions")
        TestUtils.save_dict_to_temp_file({
            "created_actions": completed_command_actions.created_actions,
        }, "completed_created_actions")

    except Exception as e:
        LoggingUtil.exception("test_command_actions_worker_subgraph", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_command_actions_worker_subgraph_error")
        raise
