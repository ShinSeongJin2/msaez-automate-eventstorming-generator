from ...mocks import ui_component_worker_subgraph_inputs
from .....subgraphs import create_ui_component_worker_subgraph, ui_component_worker_id_context
from ....terminal_util import TerminalUtil
from .....utils import LoggingUtil
from .....models import State

def run_ui_component_worker_subgraph(command_args):
    run_name = "run_ui_component_worker_subgraph"

    try:

        worker_id = '43f88581-4bae-4aaf-901b-b577be2ad3ef'

        run_subgraph = create_ui_component_worker_subgraph()
        ui_component_worker_id_context.set(worker_id)
        result: State = run_subgraph(ui_component_worker_subgraph_inputs)

        completed_ui_component = result.subgraphs.createUiComponentsModel.worker_generations.get(worker_id)

        TerminalUtil.save_dict_to_temp_file(completed_ui_component, f"{run_name}_completed_ui_component")
        TerminalUtil.save_dict_to_temp_file({
            "ui_replace_actions": [completed_ui_component.ui_replace_actions],
            "logs": result.outputs.logs,
        }, f"{run_name}_ui_replace_actions")
        TerminalUtil.check_error_logs_from_state(result, run_name)

    except Exception as e:
        LoggingUtil.exception(run_name, f"실행 실패", e)
        TerminalUtil.save_dict_to_temp_file({
            "error": str(e)
        }, f"{run_name}_error")
        raise
