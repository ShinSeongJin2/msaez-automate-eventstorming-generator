from ...systems.database.database_factory import DatabaseFactory
from ...utils import JsonUtil
from ..terminal_helper import TerminalHelper

def load_es_snapshot(command_args):
    project_id = command_args[0]
    eventstorming_id = command_args[1]
    if project_id is None or eventstorming_id is None:
        raise ValueError("Project ID and Eventstorming ID are required")

    definition_path = f"definitions/{project_id}_es_{eventstorming_id}"
    snapshot_lists_path = f"{definition_path}/snapshotLists"
    

    db_system = DatabaseFactory.get_db_system()
    snapshot_lists = db_system.get_data(snapshot_lists_path)

    sorted_snapshot_lists = sorted(list(snapshot_lists.values()), key=lambda x: x["timeStamp"], reverse=True)
    latest_snapshot = sorted_snapshot_lists[0]["snapshot"]


    TerminalHelper.save_dict_to_temp_file(JsonUtil.convert_to_json(latest_snapshot), "latest_snapshot")