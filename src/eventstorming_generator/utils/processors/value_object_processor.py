from typing import Dict, Any, List

from ..convert_case_util import CaseConvertUtil
from ..es_utils import EsUtils

class ValueObjectProcessor:
    @staticmethod
    def get_action_applied_es_value(action: Dict[str, Any], user_info: Dict[str, Any], 
                                   information: Dict[str, Any], es_value: Dict[str, Any], 
                                   callbacks: Dict[str, List]) -> None:
        """액션에 따라 ValueObject를 처리합니다"""
        if action.type == "create":
            ValueObjectProcessor._create_value_object(action, user_info, information, es_value, callbacks)
        elif action.type == "update":
            ValueObjectProcessor._update_value_object(action, user_info, information, es_value, callbacks)
    
    @staticmethod
    def _create_value_object(action: Dict[str, Any], user_info: Dict[str, Any], 
                            information: Dict[str, Any], es_value: Dict[str, Any], 
                            callbacks: Dict[str, List]) -> None:
        """ValueObject 생성 액션을 처리합니다"""
        def create_value_object_callback(es_value: Dict[str, Any], user_info: Dict[str, Any], 
                                        information: Dict[str, Any]) -> None:
            # 기본 ValueObject 객체 생성
            value_object_name = action.args.get("valueObjectName", f"ValueObject {action.ids.get('valueObjectId', '')[:4]}")
            value_object_alias = action.args.get("valueObjectAlias", "")
            aggregate_id = action.ids.get("aggregateId", "")
            value_object_id = action.ids.get("valueObjectId", EsUtils.get_uuid())
            
            # ValueObject 객체 생성
            value_object = ValueObjectProcessor._get_value_object_base(
                value_object_name, 
                value_object_alias,
                ValueObjectProcessor._get_field_descriptors(action.args.get("properties", [])),
                0, 0, value_object_id
            )
            
            # 위치 설정
            valid_position = ValueObjectProcessor._get_valid_position(es_value, action)
            value_object["elementView"]["x"] = valid_position["x"]
            value_object["elementView"]["y"] = valid_position["y"]
            
            # Aggregate의 entities에 추가
            entities = EsUtils.get_entities_for_aggregate(es_value, aggregate_id)
            entities["elements"][value_object["id"]] = value_object
            
            # 관계 생성
            ValueObjectProcessor._make_relations(action, value_object, callbacks)
        
        # 모든 객체가 적용된 후 실행할 콜백 등록
        callbacks["afterAllObjectAppliedCallBacks"].append(create_value_object_callback)
    
    @staticmethod
    def _update_value_object(action: Dict[str, Any], user_info: Dict[str, Any], 
                            information: Dict[str, Any], es_value: Dict[str, Any], 
                            callbacks: Dict[str, List]) -> None:
        """ValueObject 업데이트 액션을 처리합니다"""
        def update_value_object_callback(es_value: Dict[str, Any], user_info: Dict[str, Any], 
                                        information: Dict[str, Any]) -> None:
            target_aggregate = es_value["elements"].get(action.ids.get("aggregateId", ""), {})
            if (not target_aggregate or not target_aggregate.get("aggregateRoot") or 
                not target_aggregate["aggregateRoot"].get("entities") or 
                not target_aggregate["aggregateRoot"]["entities"].get("elements")):
                return
            
            target_value_object = target_aggregate["aggregateRoot"]["entities"]["elements"].get(action.ids.get("valueObjectId", ""))
            if not target_value_object:
                return
            
            if action.args.get("properties"):
                # 필드 머지
                target_value_object["fieldDescriptors"] = ValueObjectProcessor._merge_field_descriptors(
                    target_value_object["fieldDescriptors"],
                    action.args.get("properties", [])
                )
                target_aggregate["aggregateRoot"]["entities"]["elements"][action.ids.get("valueObjectId", "")] = target_value_object
        
        # 모든 객체가 적용된 후 실행할 콜백 등록
        callbacks["afterAllObjectAppliedCallBacks"].append(update_value_object_callback)
    
    @staticmethod
    def _get_value_object_base(name: str, display_name: str, field_descriptors: List[Dict[str, Any]], 
                              x: int, y: int, element_uuid: str = None) -> Dict[str, Any]:
        """ValueObject 기본 객체를 생성합니다"""
        element_uuid_to_use = element_uuid or EsUtils.get_uuid()
        
        return {
            "_type": "org.uengine.uml.model.vo.Class",
            "id": element_uuid_to_use,
            "name": name,
            "displayName": display_name,
            "namePascalCase": CaseConvertUtil.pascal_case(name),
            "nameCamelCase": CaseConvertUtil.camel_case(name),
            "namePlural": CaseConvertUtil.plural(name),
            "fieldDescriptors": field_descriptors,
            "operations": [],
            "elementView": {
                "_type": "org.uengine.uml.model.vo.address.Class",
                "id": element_uuid_to_use,
                "x": x,
                "y": y,
                "width": 200,
                "height": 100,
                "style": "{}",
                "titleH": 50,
                "subEdgeH": 170,
                "fieldH": 150,
                "methodH": 30
            },
            "selected": False,
            "parentOperations": [],
            "relationType": None,
            "isVO": True,
            "relations": [],
            "groupElement": None,
            "isAggregateRoot": False,
            "isAbstract": False,
            "isInterface": False
        }
    
    @staticmethod
    def _get_valid_position(es_value: Dict[str, Any], action: Dict[str, Any]) -> Dict[str, int]:
        """ValueObject의 적절한 위치를 계산합니다"""
        related_value_objects = ValueObjectProcessor._get_related_value_objects(es_value, action.ids.get("aggregateId", ""))
        return {"x": 700 + (len(related_value_objects) * 250), "y": 152}
    
    @staticmethod
    def _get_field_descriptors(properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """필드 기술자 목록을 생성합니다"""
        return [
            {
                "className": prop.get("type", "String"),
                "isCopy": False,
                "isKey": prop.get("isKey", False),
                "label": f"- {prop.get('name', '')}: {prop.get('type', 'String')}",
                "name": prop.get("name", ""),
                "nameCamelCase": CaseConvertUtil.camel_case(prop.get("name", "")),
                "namePascalCase": CaseConvertUtil.pascal_case(prop.get("name", "")),
                "displayName": prop.get("displayName", ""),
                "referenceClass": prop.get("referenceClass", None),
                "isOverrideField": prop.get("isOverrideField", False),
                "_type": "org.uengine.model.FieldDescriptor"
            }
            for prop in properties if not prop.get("isForeignProperty", False)
        ]
    
    @staticmethod
    def _merge_field_descriptors(existing_fields: List[Dict[str, Any]], new_properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """기존 필드와 새 속성을 병합합니다"""
        merged = existing_fields.copy()
        
        for new_prop in new_properties:
            if new_prop.get("isForeignProperty", False):
                continue
                
            # 기존 필드와 이름이 같은 속성이 있는지 확인
            existing_index = next((i for i, field in enumerate(merged) if field.get("name") == new_prop.get("name")), -1)
            
            if existing_index >= 0:
                # 기존 필드 업데이트
                merged[existing_index].update({
                    "className": new_prop.get("type", "String"),
                    "referenceClass": new_prop.get("referenceClass", None),
                    "isOverrideField": new_prop.get("isOverrideField", False),
                })
            else:
                # 새 필드 추가
                merged.append(ValueObjectProcessor._get_field_descriptors([new_prop])[0])
        
        return merged
        
    @staticmethod
    def _get_related_value_objects(es_value: Dict[str, Any], aggregate_id: str) -> List[Dict[str, Any]]:
        """특정 Aggregate에 있는 모든 ValueObject를 가져옵니다"""
        aggregate = es_value["elements"].get(aggregate_id, {})
        if (not aggregate.get("aggregateRoot") or 
            not aggregate["aggregateRoot"].get("entities") or 
            not aggregate["aggregateRoot"]["entities"].get("elements")):
            return []
        
        entities = aggregate["aggregateRoot"]["entities"]["elements"]
        return [
            element for element in entities.values()
            if element and element.get("_type") == "org.uengine.uml.model.vo.Class"
        ]
    
    @staticmethod
    def _make_relations(action: Dict[str, Any], value_object: Dict[str, Any], callbacks: Dict[str, List]) -> None:
        """관계를 생성합니다"""
        def make_relations_callback(es_value: Dict[str, Any], user_info: Dict[str, Any], 
                                    information: Dict[str, Any]) -> None:
            entities = EsUtils.get_entities_for_aggregate(es_value, action.ids.get("aggregateId", ""))
            source_element = entities["elements"].get(value_object["id"])
            if not source_element:
                return
            
            for field_descriptor in source_element["fieldDescriptors"]:
                matched_element = None
                for element in [e for e in entities["elements"].values() if e]:
                    if field_descriptor["className"] == element.get("name"):
                        matched_element = element
                        break
                
                if not matched_element:
                    continue
                
                # 이미 관계가 존재하는지 확인
                relation_exists = False
                for relation in [r for r in entities["relations"].values() if r]:
                    if relation.get("from") == source_element["id"] and relation.get("to") == matched_element["id"]:
                        relation_exists = True
                        break
                
                if relation_exists:
                    continue
                
                # 새 관계 생성
                ddl_relation_object = ValueObjectProcessor._get_ddl_relation_base(source_element, matched_element)
                
                if not source_element.get("relations"):
                    source_element["relations"] = []
                source_element["relations"].append(ddl_relation_object["id"])
                
                if not matched_element.get("relations"):
                    matched_element["relations"] = []
                matched_element["relations"].append(ddl_relation_object["id"])
                
                entities["relations"][ddl_relation_object["id"]] = ddl_relation_object
                
                # 필드에서 제거
                source_element["fieldDescriptors"] = [
                    fd for fd in source_element["fieldDescriptors"] 
                    if fd.get("className") != matched_element.get("name")
                ]
        
        callbacks["afterAllRelationAppliedCallBacks"].append(make_relations_callback)
    
    @staticmethod
    def _get_ddl_relation_base(from_object: Dict[str, Any], to_object: Dict[str, Any]) -> Dict[str, Any]:
        """DDL 관계 객체를 생성합니다"""
        element_uuid = EsUtils.get_uuid()
        from_id = from_object.get("id") or from_object["elementView"]["id"]
        to_id = to_object.get("id") or to_object["elementView"]["id"]
        
        return {
            "name": to_object.get("name", ""),
            "id": element_uuid,
            "_type": "org.uengine.uml.model.Relation",
            "sourceElement": from_object,
            "targetElement": to_object,
            "from": from_id,
            "to": to_id,
            "selected": False,
            "relationView": {
                "id": element_uuid,
                "style": "{\"arrow-start\":\"none\",\"arrow-end\":\"none\"}",
                "from": from_id,
                "to": to_id,
                "needReconnect": True
            },
            "sourceMultiplicity": "1",
            "targetMultiplicity": "1",
            "relationType": "Association",
            "fromLabel": "",
            "toLabel": ""
        }