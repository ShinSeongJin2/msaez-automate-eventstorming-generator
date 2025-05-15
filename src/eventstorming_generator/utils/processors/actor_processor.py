from typing import Dict, Any, List

from ..es_utils import EsUtils

class ActorProcessor:
    @staticmethod
    def get_action_applied_es_value(action: Dict[str, Any], user_info: Dict[str, Any], 
                                   information: Dict[str, Any], es_value: Dict[str, Any], 
                                   callbacks: Dict[str, List]) -> None:
        """액션에 따라 Actor를 처리합니다"""
        if action.type == "create":
            ActorProcessor._create_actor(action, user_info, information, es_value, callbacks)
    
    @staticmethod
    def _create_actor(action: Dict[str, Any], user_info: Dict[str, Any], 
                     information: Dict[str, Any], es_value: Dict[str, Any], 
                     callbacks: Dict[str, List]) -> None:
        """Actor 생성 액션을 처리합니다"""
        actor_name = action.args.get("actorName", "")
        bounded_context_id = action.ids.get("boundedContextId", "")
        actor_id = action.ids.get("actorId", EsUtils.get_uuid())
        
        # Actor 객체 생성
        actor_object = ActorProcessor._get_actor_base(user_info, actor_name, bounded_context_id, 0, 0, actor_id)
        
        # 위치 설정
        if action.args.get("relatedCommandId"):
            def set_position(es_value: Dict[str, Any], user_info: Dict[str, Any], 
                           information: Dict[str, Any]) -> None:
                command_object = es_value["elements"].get(action.args.get("relatedCommandId", ""))
                if not command_object:
                    return
                    
                valid_position = ActorProcessor._get_valid_position(command_object, actor_object)
                actor_object["elementView"]["x"] = valid_position["x"]
                actor_object["elementView"]["y"] = valid_position["y"]
                es_value["elements"][actor_object["id"]] = actor_object
            
            callbacks["afterAllObjectAppliedCallBacks"].append(set_position)
        
        # Actor 객체 추가
        es_value["elements"][actor_object["id"]] = actor_object
    
    @staticmethod
    def make_actor_to_command(es_value: Dict[str, Any], action: Dict[str, Any], 
                            command_object: Dict[str, Any], user_info: Dict[str, Any]) -> None:
        """Command와 연결된 Actor를 생성합니다"""
        # 이미 연결된 정책이 있는지 확인
        if ActorProcessor._get_related_policies(es_value, command_object):
            return
            
        # actor가 지정되지 않았으면 중단
        if not action.args.get("actor"):
            return
            
        # Actor 생성
        actor_base = ActorProcessor._get_actor_base(
            user_info, action.args.get("actor"), action.ids.get("boundedContextId"), 0, 0
        )
        
        # 위치 계산
        valid_position = ActorProcessor._get_valid_position(command_object, actor_base)
        actor_base["elementView"]["x"] = valid_position["x"]
        actor_base["elementView"]["y"] = valid_position["y"]
        
        # Actor 객체 추가
        es_value["elements"][actor_base["id"]] = actor_base
    
    @staticmethod
    def _get_related_policies(es_value: Dict[str, Any], command_object: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Command와 연결된 Policy 객체 목록을 가져옵니다"""
        return [
            relation for relation in es_value["relations"].values()
            if (relation and 
                relation.get("targetElement", {}).get("id") == command_object["id"] and
                relation.get("sourceElement", {}).get("_type") == "org.uengine.modeling.model.Policy")
        ]
    
    @staticmethod
    def _get_actor_base(user_info: Dict[str, Any], actor_name: str, 
                       bounded_context_id: str, x: int, y: int, 
                       element_uuid: str = None) -> Dict[str, Any]:
        """Actor 기본 객체를 생성합니다"""
        element_uuid_to_use = element_uuid or EsUtils.get_uuid()
        
        return {
            "_type": "org.uengine.modeling.model.Actor",
            "author": user_info.get("uid", ""),
            "boundedContext": {
                "id": bounded_context_id
            },
            "description": None,
            "id": element_uuid_to_use,
            "elementView": {
                "_type": "org.uengine.modeling.model.Actor",
                "height": 100,
                "id": element_uuid_to_use,
                "style": "{}",
                "width": 100,
                "x": x,
                "y": y
            },
            "innerAggregate": {
                "command": [],
                "event": [],
                "external": [],
                "policy": [],
                "view": [],
            },
            "name": actor_name,
            "oldName": "",
            "rotateStatus": False
        }
    
    @staticmethod
    def _get_valid_position(command_object: Dict[str, Any], actor_object: Dict[str, Any]) -> Dict[str, int]:
        """Actor의 적절한 위치를 계산합니다"""
        return {
            "x": command_object["elementView"]["x"] - int(command_object["elementView"]["width"]/2) - int(actor_object["elementView"]["width"]/2) + 19,
            "y": command_object["elementView"]["y"]
        }
