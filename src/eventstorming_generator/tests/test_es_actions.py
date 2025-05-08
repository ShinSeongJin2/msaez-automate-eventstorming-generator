from ..models import EsValueModel
from ..utils.es_actions_util import EsActionsUtil
from .mocks import actions, user_info, information

def test_bounded_context_creation():
    """BoundedContext 생성 테스트"""
    try:
        es_value = EsValueModel()
        
        result = EsActionsUtil.apply_actions(es_value, actions, user_info, information)
        
        print("=== 테스트 결과 ===")
        print(f"Elements 수: {len(result['elements'])}")
        
        for element_id, element in result['elements'].items():
            if element['_type'] == "org.uengine.modeling.model.BoundedContext":
                print(f"생성된 BoundedContext: {element['name']} (ID: {element_id})")
                print(f"  - 위치: x={element['elementView']['x']}, y={element['elementView']['y']}")
                print(f"  - 포트: {element['portGenerated']}")
        
        print(result)
    except Exception as e:
        print(f"테스트 실패: {str(e)}")
        raise