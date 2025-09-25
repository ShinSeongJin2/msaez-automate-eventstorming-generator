from ...models import EsValueModel
from ...utils import ESFakeActionsUtil
from ..mocks import actions_for_fake_test
from ..run_util import RunUtil
from ...utils import LoggingUtil

def run_fake_actions_util():
    run_name = "run_fake_actions_util"

    try:

        result = ESFakeActionsUtil.add_fake_actions(actions_for_fake_test, EsValueModel())
        RunUtil.save_dict_to_temp_file(result, run_name)

    except Exception as e:
        LoggingUtil.exception(run_name, f"실행 실패", e)
        RunUtil.save_dict_to_temp_file({
            "error": str(e),
            "actions": actions_for_fake_test
        }, f"{run_name}_error")
        raise