from ...models import EsValueModel
from ...utils import ESFakeActionsUtil
from ..mocks import actions_for_fake_test
from ..test_utils import TestUtils

def test_fake_actions_util():
    try:

        result = ESFakeActionsUtil.add_fake_actions(actions_for_fake_test, EsValueModel())
        TestUtils.save_dict_to_temp_file(result, "test_fake_actions_util")

    except Exception as e:
        print(f"테스트 실패: {str(e)}")
        TestUtils.save_dict_to_temp_file({
            "error": str(e),
            "actions": actions_for_fake_test
        }, "test_fake_actions_util_error")
        raise