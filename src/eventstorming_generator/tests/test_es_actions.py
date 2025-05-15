from ..models import EsValueModel
from ..utils import EsActionsUtil
from .mocks import actions, user_info, information
from .test_utils import TestUtils

def test_es_value_creation():
    try:

        es_value = EsValueModel()
        result = EsActionsUtil.apply_actions(es_value, actions, user_info, information)
        TestUtils.save_dict_to_temp_file(result, "test_es_value_creation")
        TestUtils.save_es_summarize_result_to_temp_file(result, "test_es_value_creation")

    except Exception as e:
        print(f"테스트 실패: {str(e)}")
        TestUtils.save_dict_to_temp_file({
            "error": str(e),
            "actions": actions,
            "user_info": user_info,
            "information": information
        }, "test_es_value_creation_error")
        raise