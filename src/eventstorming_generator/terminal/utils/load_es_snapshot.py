from ...systems import FirebaseSystem
from ...utils import JsonUtil
from ..terminal_helper import TerminalHelper

def load_es_snapshot(command_args):
    project_id = command_args[0]
    eventstorming_id = command_args[1]
    if project_id is None or eventstorming_id is None:
        raise ValueError("Project ID and Eventstorming ID are required")

    definition_path = f"definitions/{project_id}_es_{eventstorming_id}"
    snapshot_lists_path = f"{definition_path}/snapshotLists"
    

    firebase = FirebaseSystem.instance()
    snapshot_lists = firebase.get_data(snapshot_lists_path)

    sorted_snapshot_lists = sorted(list(snapshot_lists.values()), key=lambda x: x["timeStamp"], reverse=True)
    latest_snapshot = sorted_snapshot_lists[0]["snapshot"]


    TerminalHelper.save_dict_to_temp_file(JsonUtil.convert_to_json(latest_snapshot), "latest_snapshot")