from typing import Dict, Any, List
from convert_case import camel_case, pascal_case
from pluralizer import Pluralizer

from ..es_utils import EsUtils

pluralizer = Pluralizer()

class PolicyProcessor:
    @staticmethod
    def get_action_applied_es_value(action: Dict[str, Any], user_info: Dict[str, Any], 
                                   information: Dict[str, Any], es_value: Dict[str, Any], 
                                   callbacks: Dict[str, List]) -> None:
        """액션 유형에 따라 Policy를 처리합니다"""
        # 추후 필요시 Policy 관련 액션 처리 로직 구현
        pass
    
    @staticmethod
    def create_new_policy(es_value: Dict[str, Any], user_info: Dict[str, Any], 
                         event_object: Dict[str, Any], command_id: str, update_reason: str, 
                         name: str = None, display_name: str = None) -> None:
        """이벤트와 명령 사이에 새로운 Policy를 생성합니다"""
        command_object = es_value["elements"].get(command_id)
        if not command_object or not event_object:
            return
            
        # 이벤트와 명령이 같은 Aggregate에 속하는 경우 생성하지 않음
        if command_object.get("aggregate", {}).get("id") == event_object.get("aggregate", {}).get("id"):
            return
            
        # Policy 기본 객체 생성
        policy_name = name if name else f"{command_object.get('name', '')} Policy"
        policy_display_name = display_name if display_name else f"{command_object.get('name', '')} Policy"
        
        policy_object = PolicyProcessor._get_policy_base(
            user_info, policy_name, policy_display_name, 
            command_object.get("boundedContext", {}).get("id", ""), 
            update_reason, 0, 0
        )
        
        # Policy 객체 등록
        es_value["elements"][policy_object["id"]] = policy_object
        
        # Event-Policy 관계 생성
        PolicyProcessor._make_event_to_policy_relation(es_value, event_object, policy_object)
        
        # Policy-Command 관계 생성
        PolicyProcessor._make_policy_to_command_relation(es_value, policy_object, command_object)
        
        # 유효한 위치 계산 및 설정
        valid_position = PolicyProcessor._get_valid_position(es_value, command_object.get("aggregate", {}).get("id", ""), policy_object)
        policy_object["elementView"]["x"] = valid_position["x"]
        policy_object["elementView"]["y"] = valid_position["y"]
        
        # 관련 Actor 제거
        PolicyProcessor._remove_related_actors(es_value, policy_object)
    
    @staticmethod
    def _get_policy_base(user_info: Dict[str, Any], name: str, display_name: str, 
                        bounded_context_id: str, update_reason: str, 
                        x: int, y: int, element_uuid: str = None) -> Dict[str, Any]:
        """Policy 기본 객체를 생성합니다"""
        element_uuid_to_use = element_uuid or EsUtils.get_uuid()
        
        return {
            "id": element_uuid_to_use,
            "author": user_info.get("uid", ""),
            "boundedContext": {
                "id": bounded_context_id
            },
            "description": update_reason if update_reason else None,
            "elementView": {
                "height": 115,
                "width": 100,
                "x": x,
                "y": y,
                "id": element_uuid_to_use,
                "style": "{}",
                "_type": "org.uengine.modeling.model.Policy"
            },
            "fieldDescriptors": [],
            "hexagonalView": {
                "height": 20,
                "id": element_uuid_to_use,
                "style": "{}",
                "subWidth": 100,
                "width": 20,
                "_type": "org.uengine.modeling.model.PolicyHexagonal"
            },
            "isSaga": False,
            "name": name,
            "displayName": display_name,
            "nameCamelCase": camel_case(name),
            "namePascalCase": pascal_case(name),
            "namePlural": pluralizer.plural(camel_case(name)),
            "oldName": "",
            "rotateStatus": False,
            "_type": "org.uengine.modeling.model.Policy"
        }
    
    @staticmethod
    def _make_event_to_policy_relation(es_value: Dict[str, Any], event_object: Dict[str, Any], 
                                      policy_object: Dict[str, Any]) -> None:
        """이벤트와 정책 사이의 관계를 생성합니다"""
        if not es_value["elements"].get(event_object["id"]) or not es_value["elements"].get(policy_object["id"]):
            return
            
        event_policy_relation = EsUtils.getEventStormingRelationObjectBase(
            es_value["elements"][event_object["id"]], es_value["elements"][policy_object["id"]]
        )
        
        es_value["relations"][event_policy_relation["id"]] = event_policy_relation
    
    @staticmethod
    def _make_policy_to_command_relation(es_value: Dict[str, Any], policy_object: Dict[str, Any], 
                                        command_object: Dict[str, Any]) -> None:
        """정책과 명령 사이의 관계를 생성합니다"""
        if not es_value["elements"].get(policy_object["id"]) or not es_value["elements"].get(command_object["id"]):
            return
            
        policy_command_relation = EsUtils.getEventStormingRelationObjectBase(
            es_value["elements"][policy_object["id"]], es_value["elements"][command_object["id"]]
        )
        
        es_value["relations"][policy_command_relation["id"]] = policy_command_relation
    
    @staticmethod
    def _get_valid_position(es_value: Dict[str, Any], aggregate_id: str, 
                           policy_object: Dict[str, Any]) -> Dict[str, int]:
        """Policy의 적절한 위치를 계산합니다"""
        related_commands = PolicyProcessor._get_related_commands(es_value, policy_object)
        
        if len(related_commands) <= 0:
            current_aggregate = es_value["elements"].get(aggregate_id)
            if not current_aggregate:
                return {"x": 0, "y": 0}
                
            return {
                "x": current_aggregate["elementView"]["x"] - int(current_aggregate["elementView"]["width"]/2) - 148,
                "y": current_aggregate["elementView"]["y"] - int(current_aggregate["elementView"]["height"]/2)
            }
        else:
            min_x = min(command["elementView"]["x"] for command in related_commands)
            max_y = max(command["elementView"]["y"] for command in related_commands)
            
            max_y_commands = [command for command in related_commands if command["elementView"]["y"] == max_y]
            if not max_y_commands:
                return {"x": min_x - 150, "y": max_y}
                
            max_y_command = max_y_commands[0]
            return {
                "x": min_x - int(policy_object["elementView"]["width"]/2) - int(max_y_command["elementView"]["width"]/2) - 19,
                "y": max_y
            }
    
    @staticmethod
    def _remove_related_actors(es_value: Dict[str, Any], policy_object: Dict[str, Any]) -> None:
        """Policy 위치와 겹치는 Actor를 제거합니다"""
        policy_left = policy_object["elementView"]["x"] - policy_object["elementView"]["width"]/2
        policy_right = policy_object["elementView"]["x"] + policy_object["elementView"]["width"]/2 + 30
        policy_top = policy_object["elementView"]["y"] - policy_object["elementView"]["height"]/2
        policy_bottom = policy_object["elementView"]["y"] + policy_object["elementView"]["height"]/2
        
        for element_id, element in list(es_value["elements"].items()):
            if (element and element.get("_type") == "org.uengine.modeling.model.Actor" and
                element.get("boundedContext", {}).get("id") == policy_object.get("boundedContext", {}).get("id") and
                policy_top <= element["elementView"]["y"] <= policy_bottom and
                policy_left <= element["elementView"]["x"] <= policy_right):
                del es_value["elements"][element_id]
    
    @staticmethod
    def _get_related_commands(es_value: Dict[str, Any], policy_object: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Policy와 연관된 명령을 찾습니다"""
        related_commands = []
        
        for relation in es_value["relations"].values():
            if (relation and 
                relation.get("_type") == "org.uengine.modeling.model.Relation" and
                (relation.get("sourceElement", {}).get("id") == policy_object["id"] or 
                 relation.get("sourceElement", {}).get("id") == policy_object["elementView"]["id"]) and
                relation.get("targetElement", {}).get("_type") == "org.uengine.modeling.model.Command"):
                command = es_value["elements"].get(relation["targetElement"]["id"])
                if command:
                    related_commands.append(command)
        
        return related_commands