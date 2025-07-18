from typing import Dict, Any, List

from ..convert_case_util import CaseConvertUtil
from ..es_utils import EsUtils

class EnumerationProcessor:
    @staticmethod
    def get_action_applied_es_value(action: Dict[str, Any], user_info: Dict[str, Any], 
                                   information: Dict[str, Any], es_value: Dict[str, Any], 
                                   callbacks: Dict[str, List]) -> None:
        """액션에 따라 Enumeration을 처리합니다"""
        if action.type == "create":
            EnumerationProcessor._create_enumeration(action, user_info, information, es_value, callbacks)
        elif action.type == "update":
            EnumerationProcessor._update_enumeration(action, user_info, information, es_value, callbacks)
    
    @staticmethod
    def _create_enumeration(action: Dict[str, Any], user_info: Dict[str, Any], 
                           information: Dict[str, Any], es_value: Dict[str, Any], 
                           callbacks: Dict[str, List]) -> None:
        """Enumeration 생성 액션을 처리합니다"""
        def create_enumeration_callback(es_value: Dict[str, Any], user_info: Dict[str, Any], 
                                       information: Dict[str, Any]) -> None:
            # 기본 Enumeration 객체 생성
            enumeration_name = action.args.get("enumerationName", f"Enumeration {action.ids.get('enumerationId', '')[:4]}")
            enumeration_alias = action.args.get("enumerationAlias", "")
            aggregate_id = action.ids.get("aggregateId", "")
            enumeration_id = action.ids.get("enumerationId", EsUtils.get_uuid())
            source_reference = action.args.get("sourceReferences", [])

            # Enumeration 값 목록 변환
            properties = action.args.get("properties", [])
            items = [{"value": prop.get("name"), "sourceReferences": prop.get("sourceReferences", [])} for prop in properties]
            
            # Enumeration 객체 생성
            enumeration = EnumerationProcessor._get_enumeration_base(
                enumeration_name, 
                enumeration_alias,
                items,
                0, 0, enumeration_id, source_reference
            )
            
            # 위치 설정
            valid_position = EnumerationProcessor._get_valid_position(es_value, action)
            enumeration["elementView"]["x"] = valid_position["x"]
            enumeration["elementView"]["y"] = valid_position["y"]
            
            # Aggregate의 entities에 추가
            entities = EsUtils.get_entities_for_aggregate(es_value, aggregate_id)
            entities["elements"][enumeration["id"]] = enumeration
        
        # 모든 객체가 적용된 후 실행할 콜백 등록
        callbacks["afterAllObjectAppliedCallBacks"].append(create_enumeration_callback)
    
    @staticmethod
    def _update_enumeration(action: Dict[str, Any], user_info: Dict[str, Any], 
                           information: Dict[str, Any], es_value: Dict[str, Any], 
                           callbacks: Dict[str, List]) -> None:
        """Enumeration 업데이트 액션을 처리합니다"""
        def update_enumeration_callback(es_value: Dict[str, Any], user_info: Dict[str, Any], 
                                       information: Dict[str, Any]) -> None:
            target_aggregate = es_value["elements"].get(action.ids.get("aggregateId", ""), {})
            if (not target_aggregate or not target_aggregate.get("aggregateRoot") or 
                not target_aggregate["aggregateRoot"].get("entities") or 
                not target_aggregate["aggregateRoot"]["entities"].get("elements")):
                return
            
            target_enumeration = target_aggregate["aggregateRoot"]["entities"]["elements"].get(action.ids.get("enumerationId", ""))
            if not target_enumeration:
                return
            
            if action.args.get("properties"):
                # 새 항목 추가
                items = [{"value": prop.get("name"), "sourceReferences": prop.get("sourceReferences", [])} for prop in action.args.get("properties", [])]
                target_enumeration["items"].extend(items)
                target_aggregate["aggregateRoot"]["entities"]["elements"][action.ids.get("enumerationId", "")] = target_enumeration
        
        # 모든 객체가 적용된 후 실행할 콜백 등록
        callbacks["afterAllObjectAppliedCallBacks"].append(update_enumeration_callback)
    
    @staticmethod
    def _get_enumeration_base(name: str, display_name: str, items: List[Dict[str, str]], 
                             x: int, y: int, element_uuid: str = None, 
                             source_reference: List[List[List[Any]]] = []) -> Dict[str, Any]:
        """Enumeration 기본 객체를 생성합니다"""
        element_uuid_to_use = element_uuid or EsUtils.get_uuid()
        
        return {
            "_type": "org.uengine.uml.model.enum",
            "id": element_uuid_to_use,
            "name": name,
            "displayName": display_name,
            "nameCamelCase": CaseConvertUtil.camel_case(name),
            "namePascalCase": CaseConvertUtil.pascal_case(name),
            "namePlural": CaseConvertUtil.plural(name),
            "elementView": {
                "_type": "org.uengine.uml.model.enum",
                "id": element_uuid_to_use,
                "x": x,
                "y": y,
                "width": 200,
                "height": 100,
                "style": "{}",
                "titleH": 50,
                "subEdgeH": 50
            },
            "selected": False,
            "items": items,
            "useKeyValue": False,
            "relations": [],
            "sourceReferences": source_reference
        }
    
    @staticmethod
    def _get_valid_position(es_value: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, int]:
        """Enumeration의 적절한 위치를 계산합니다"""
        related_enumerations = EnumerationProcessor._get_related_enumerations(es_value, action.ids.get("aggregateId", ""))
        return {"x": 700 + (len(related_enumerations) * 250), "y": 456}
    
    @staticmethod
    def _get_related_enumerations(es_value: Dict[str, Any], aggregate_id: str) -> List[Dict[str, Any]]:
        """특정 Aggregate에 있는 모든 Enumeration을 가져옵니다"""
        aggregate = es_value["elements"].get(aggregate_id, {})
        if (not aggregate.get("aggregateRoot") or 
            not aggregate["aggregateRoot"].get("entities") or 
            not aggregate["aggregateRoot"]["entities"].get("elements")):
            return []
        
        entities = aggregate["aggregateRoot"]["entities"]["elements"]
        return [
            element for element in entities.values()
            if element and element.get("_type") == "org.uengine.uml.model.enum"
        ]