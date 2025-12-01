from typing import Dict, Any, List

from ..es_utils import EsUtils
from ....models import ActionModel

class BoundedContextProcessor:
    @staticmethod
    def get_action_applied_es_value(action: ActionModel, user_id: str, project_id: str, 
                                   es_value: Dict[str, Any], callbacks: Dict[str, List]) -> None:
        """액션에 따라 BoundedContext를 처리합니다"""
        if action.type == "create":
            BoundedContextProcessor._create_bounded_context(action, user_id, project_id, es_value, callbacks)
    
    @staticmethod
    def _create_bounded_context(action: ActionModel, user_id: str, project_id: str, es_value: Dict[str, Any], 
                              callbacks: Dict[str, List]) -> None:
        """BoundedContext 생성 액션을 처리합니다"""
        # 기본 BoundedContext 객체 생성
        bc_name = action.args.get("boundedContextName", "BoundedContext")
        bc_alias = action.args.get("boundedContextAlias", "")
        description = action.args.get("description", "")
        bounded_context_id = action.ids.get("boundedContextId", EsUtils.get_uuid())
        
        # 포트 번호 생성
        port_number = BoundedContextProcessor._get_valid_port_number(es_value)
        
        # BoundedContext 객체 생성
        bounded_context_object = BoundedContextProcessor._get_bounded_context_base(
            user_id, project_id, bc_name, bc_alias, port_number, 
            description, 0, 0, bounded_context_id
        )
        
        # 위치 설정
        valid_position = BoundedContextProcessor._get_valid_position(es_value, bounded_context_object)
        bounded_context_object["elementView"]["x"] = valid_position["x"]
        bounded_context_object["elementView"]["y"] = valid_position["y"]
        
        # es_value에 추가
        if "elements" not in es_value:
            es_value["elements"] = {}
        es_value["elements"][bounded_context_object["id"]] = bounded_context_object
    
    @staticmethod
    def _get_valid_port_number(es_value: Dict[str, Any]) -> int:
        """사용 가능한 포트 번호를 생성합니다"""
        bounded_contexts = EsUtils.get_all_bounded_contexts(es_value)
        if not bounded_contexts:
            return 8080
        
        max_port_number = 8079  # 기본값 8080 - 1
        for bc in bounded_contexts:
            port = bc.get("portGenerated", 0)
            if port > max_port_number:
                max_port_number = port
        
        return max_port_number + 1
    
    @staticmethod
    def _get_bounded_context_base(user_id: str, project_id: str,
                                name: str, display_name: str, port_number: int, 
                                description: str, x: int, y: int, element_uuid: str) -> Dict[str, Any]:
        """BoundedContext 기본 객체를 생성합니다"""
        element_uuid_to_use = element_uuid or EsUtils.get_uuid()
        
        return {
            "_type": "org.uengine.modeling.model.BoundedContext",
            "aggregates": [],
            "author": user_id,
            "description": description,
            "id": element_uuid_to_use,
            "elementView": {
                "_type": "org.uengine.modeling.model.BoundedContext",
                "height": 590,
                "id": element_uuid_to_use,
                "style": "{}",
                "width": 560,
                "x": x,
                "y": y,
            },
            "gitURL": None,
            "hexagonalView": {
                "_type": "org.uengine.modeling.model.BoundedContextHexagonal",
                "height": 350,
                "id": element_uuid_to_use,
                "style": "{}",
                "width": 350,
                "x": 235,
                "y": 365
            },
            "members": [],
            "name": name,
            "traceName": name,
            "displayName": display_name,
            "oldName": "",
            "policies": [],
            "portGenerated": port_number,
            "preferredPlatform": "template-spring-boot",
            "preferredPlatformConf": {},
            "rotateStatus": False,
            "tempId": "",
            "templatePerElements": {},
            "views": [],
            "definitionId": project_id
        }
    
    @staticmethod
    def _get_valid_position(es_value: Dict[str, Any], bounded_context_object: Dict[str, Any]) -> Dict[str, int]:
        """BoundedContext의 적절한 위치를 계산합니다"""
        # 첫 번째 BoundedContext인 경우 기본 위치 반환
        bounded_contexts = EsUtils.get_all_bounded_contexts(es_value)
        if not bounded_contexts:
            return {"x": 600, "y": 450}
        
        # 가장 아래쪽 행에서 가장 오른쪽 BoundedContext 찾기
        max_y_bounded_context = max(bounded_contexts, key=lambda bc: bc["elementView"]["y"])
        max_y = max_y_bounded_context["elementView"]["y"]
        
        # max_y 범위에 있는 BoundedContext들 찾기
        bc_height = max_y_bounded_context["elementView"]["height"]
        bounded_contexts_in_max_y_range = [
            bc for bc in bounded_contexts
            if bc["elementView"]["y"] >= max_y - bc_height/2 and
               bc["elementView"]["y"] <= max_y + bc_height/2
        ]
        
        # max_y 범위에서 가장 오른쪽 BoundedContext 찾기
        max_x_bounded_context = max(bounded_contexts_in_max_y_range, key=lambda bc: bc["elementView"]["x"])
        max_x = max_x_bounded_context["elementView"]["x"]
        
        # 새 BoundedContext의 x 위치 계산
        new_x = max_x + max_x_bounded_context["elementView"]["width"]/2 + bounded_context_object["elementView"]["width"]/2 + 25
        
        # 최대 x 제한 확인
        bounded_context_max_x_limit = 1950
        if new_x <= bounded_context_max_x_limit:
            # 같은 행에 배치
            new_y = BoundedContextProcessor._get_valid_y_position(bounded_contexts, new_x)
            return {"x": new_x, "y": new_y}
        else:
            # 새로운 행에 배치
            return {"x": 600, "y": BoundedContextProcessor._get_valid_y_position(bounded_contexts, 450)}
    
    @staticmethod
    def _get_valid_y_position(bounded_contexts: List[Dict[str, Any]], x_pos: int) -> int:
        """주어진 x 위치에서 유효한 y 위치를 계산합니다"""
        base_bc_width = 560
        base_bc_height = 590
        
        # x_pos 위치와 겹치는 BoundedContext들 찾기
        target_bounded_contexts = [
            bc for bc in bounded_contexts
            if bc["elementView"]["x"] - bc["elementView"]["width"]/2 <= x_pos + base_bc_width/2 and
               bc["elementView"]["x"] + bc["elementView"]["width"]/2 >= x_pos - base_bc_width/2
        ]
        
        if not target_bounded_contexts:
            return 450
        
        # 겹치는 BoundedContext들 중 가장 아래쪽 위치 계산
        max_y_height_sum = max([
            bc["elementView"]["y"] + bc["elementView"]["height"]/2
            for bc in target_bounded_contexts
        ])
        
        return max_y_height_sum + 25 + base_bc_height/2 