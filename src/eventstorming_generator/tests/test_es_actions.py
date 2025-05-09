from ..models import EsValueModel
from ..utils import EsActionsUtil
from .mocks import actions, user_info, information
from .save_to_temp_file import save_to_temp_file

def test_es_value_creation():
    try:
        es_value = EsValueModel()
        result = EsActionsUtil.apply_actions(es_value, actions, user_info, information)
        save_to_temp_file(result, "test_es_value_creation")
    except Exception as e:
        print(f"테스트 실패: {str(e)}")
        raise