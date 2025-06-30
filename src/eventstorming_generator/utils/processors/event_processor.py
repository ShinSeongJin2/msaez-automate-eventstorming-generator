from typing import Dict, Any, List

from ..convert_case_util import CaseConvertUtil
from ..es_utils import EsUtils

class EventProcessor:
    @staticmethod
    def get_action_applied_es_value(action: Dict[str, Any], user_info: Dict[str, Any], 
                                   information: Dict[str, Any], es_value: Dict[str, Any], 
                                   callbacks: Dict[str, List]) -> None:
        """액션 유형에 따라 Event를 생성하거나 업데이트합니다"""
        if action.get("type") == "create":
            EventProcessor._create_event(action, user_info, information, es_value, callbacks)
        elif action.get("type") == "update":
            EventProcessor._update_event(action, user_info, information, es_value, callbacks)
    
    @staticmethod
    def _create_event(action: Dict[str, Any], user_info: Dict[str, Any], 
                     information: Dict[str, Any], es_value: Dict[str, Any], 
                     callbacks: Dict[str, List]) -> None:
        """새로운 Event를 생성합니다"""
        event_name = action.get("args", {}).get("eventName", "")
        event_alias = action.get("args", {}).get("eventAlias", "")
        bounded_context_id = action.get("ids", {}).get("boundedContextId", "")
        aggregate_id = action.get("ids", {}).get("aggregateId", "")
        event_id = action.get("ids", {}).get("eventId", "")
        
        # 기본 이벤트 객체 생성
        event_object = EventProcessor._get_event_base(
            user_info, event_name, event_alias, bounded_context_id, aggregate_id, 0, 0, event_id
        )
        
        # 유효한 위치 계산
        valid_position = EventProcessor._get_valid_position(es_value, action, event_object)
        event_object["elementView"]["x"] = valid_position["x"]
        event_object["elementView"]["y"] = valid_position["y"]
        
        # es_value에 추가
        es_value["elements"][event_object["id"]] = event_object
        
        # Aggregate 크기 조정
        EsUtils.resize_aggregate_vertically(es_value, event_object)
        
        # 필드 생성을 위한 콜백 등록
        def set_field_descriptors_callback(es_value_cb: Dict[str, Any], user_info_cb: Dict[str, Any], 
                                         information_cb: Dict[str, Any]) -> None:
            event_obj = es_value_cb["elements"].get(event_object["id"])
            if event_obj:
                event_obj["fieldDescriptors"] = EventProcessor._get_aggregate_field_descriptors(
                    es_value_cb, action, event_obj
                )
                
        callbacks["afterAllRelationAppliedCallBacks"].append(set_field_descriptors_callback)
    
    @staticmethod
    def _update_event(action: Dict[str, Any], user_info: Dict[str, Any], 
                     information: Dict[str, Any], es_value: Dict[str, Any], 
                     callbacks: Dict[str, List]) -> None:
        """기존 Event를 업데이트합니다"""
        event_id = action.get("ids", {}).get("eventId", "")
        event_object = es_value["elements"].get(event_id)
        
        if not event_object:
            return
            
    @staticmethod
    def _get_event_base(user_info: Dict[str, Any], name: str, display_name: str, 
                       bounded_context_id: str, aggregate_id: str, 
                       x: int, y: int, element_uuid: str = None) -> Dict[str, Any]:
        """이벤트 기본 객체를 생성합니다"""
        element_uuid_to_use = element_uuid or EsUtils.get_uuid()
        
        return {
            "alertURL": "/static/image/symbol/alert-icon.png",
            "author": user_info.get("uid", ""),
            "checkAlert": True,
            "description": None,
            "id": element_uuid_to_use,
            "elementView": {
                "angle": 0,
                "height": 115,
                "id": element_uuid_to_use,
                "style": "{}",
                "width": 100,
                "x": x, 
                "y": y, 
                "_type": "org.uengine.modeling.model.Event"
            },
            "fieldDescriptors": [],
            "hexagonalView": {
                "height": 0,
                "id": element_uuid_to_use,
                "style": "{}",
                "width": 0,
                "x": 0,
                "y": 0,
                "_type": "org.uengine.modeling.model.EventHexagonal"
            },
            "name": name,
            "displayName": display_name,
            "nameCamelCase": CaseConvertUtil.camel_case(name),
            "namePascalCase": CaseConvertUtil.pascal_case(name),
            "namePlural": "",
            "relationCommandInfo": [],
            "relationPolicyInfo": [],
            "rotateStatus": False,
            "selected": False,
            "trigger": "@PostPersist",
            "_type": "org.uengine.modeling.model.Event",
            "aggregate": {
                "id": aggregate_id,
            },
            "boundedContext": {
                "id": bounded_context_id
            }
        }
        
    @staticmethod
    def _get_valid_position(es_value: Dict[str, Any], action: Dict[str, Any], 
                           event_object: Dict[str, Any]) -> Dict[str, int]:
        """이벤트의 유효한 위치를 계산합니다"""
        events = EsUtils.get_aggregate_events(es_value, action.get("ids", {}).get("aggregateId", ""))
        
        if len(events) <= 0:
            # 해당 Aggregate의 첫 번째 이벤트일 경우
            current_aggregate = es_value["elements"].get(action.get("ids", {}).get("aggregateId", ""))
            if not current_aggregate:
                return {"x": 0, "y": 0}
                
            return {
                "x": current_aggregate["elementView"]["x"] + int(current_aggregate["elementView"]["width"]/2) + 29,
                "y": current_aggregate["elementView"]["y"] - int(current_aggregate["elementView"]["height"]/2)
            }
        else:
            # 기존 이벤트가 있을 경우 가장 아래에 위치
            max_x = max(event["elementView"]["x"] for event in events)
            max_y = max(event["elementView"]["y"] for event in events)
            
            max_y_events = [event for event in events if event["elementView"]["y"] == max_y]
            if not max_y_events:
                return {"x": max_x, "y": max_y + 100}
                
            max_y_event = max_y_events[0]
            return {
                "x": max_x,
                "y": max_y + int(max_y_event["elementView"]["height"]/2) + int(event_object["elementView"]["height"]/2) + 14
            }
            
    @staticmethod
    def _get_aggregate_field_descriptors(es_value: Dict[str, Any], action: Dict[str, Any], 
                                        event_object: Dict[str, Any]) -> List[Dict[str, Any]]:
        """이벤트의 필드 기술자를 생성합니다"""
        # 액션에서 속성이 지정되었을 경우 해당 속성 사용
        if action.get("args", {}).get("properties"):
            return [
                {
                    "className": prop.get("type") or "String",
                    "isCopy": False,
                    "isKey": prop.get("isKey") or False,
                    "name": prop.get("name", ""),
                    "nameCamelCase": CaseConvertUtil.camel_case(prop.get("name", "")),
                    "namePascalCase": CaseConvertUtil.pascal_case(prop.get("name", "")),
                    "displayName": prop.get("displayName", ""),
                    "_type": "org.uengine.model.FieldDescriptor"
                }
                for prop in action["args"]["properties"]
            ]
            
        # 속성이 지정되지 않았을 경우 Aggregate의 필드 사용
        target_field_descriptors = es_value["elements"].get(
            action.get("ids", {}).get("aggregateId", ""), {}
        ).get("aggregateRoot", {}).get("fieldDescriptors", [])
        
        # Delete 커맨드와 연결된 이벤트일 경우 키 필드만 사용
        if EsUtils.is_related_by_delete_command(es_value, event_object):
            target_field_descriptors = [
                field for field in target_field_descriptors
                if field.get("isKey") or False
            ]
            
        return [
            {
                "className": prop.get("className", "String"),
                "isCopy": False,
                "isKey": prop.get("isKey") or False,
                "name": prop.get("name", ""),
                "nameCamelCase": prop.get("nameCamelCase", ""),
                "namePascalCase": prop.get("namePascalCase", ""),
                "displayName": prop.get("displayName", ""),
                "_type": "org.uengine.model.FieldDescriptor"
            }
            for prop in target_field_descriptors
        ]