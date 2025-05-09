from ..models import EsValueModel
from ..utils import EsActionsUtil
from .mocks import actions, user_info, information

def test_es_value_creation():
    """ES Value 생성 테스트"""
    try:
        es_value = EsValueModel()
        
        result = EsActionsUtil.apply_actions(es_value, actions, user_info, information)
        
        print("=== 테스트 결과 ===")
        print(result.model_dump_json(indent=4))
        
        with open(".temp/test_es_actions_output.json", "w") as f:
            f.write(result.model_dump_json(indent=4))
        print("test_es_actions_output.json 파일에 생성 결과 저장 완료")
    except Exception as e:
        print(f"테스트 실패: {str(e)}")
        raise