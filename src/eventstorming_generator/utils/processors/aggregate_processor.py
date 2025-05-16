from typing import Dict, Any, List

from ..convert_case_util import CaseConvertUtil
from ..es_utils import EsUtils

class AggregateProcessor:
    @staticmethod
    def get_action_applied_es_value(action: Dict[str, Any], user_info: Dict[str, Any], 
                                   information: Dict[str, Any], es_value: Dict[str, Any], 
                                   callbacks: Dict[str, List]) -> None:
        """액션에 따라 Aggregate를 처리합니다"""
        if action.type == "create":
            AggregateProcessor._create_aggregate(action, user_info, information, es_value, callbacks)
        elif action.type == "update":
            AggregateProcessor._update_aggregate(action, user_info, information, es_value, callbacks)
    
    @staticmethod
    def _create_aggregate(action: Dict[str, Any], user_info: Dict[str, Any], 
                         information: Dict[str, Any], es_value: Dict[str, Any], 
                         callbacks: Dict[str, List]) -> None:
        """Aggregate 생성 액션을 처리합니다"""
        # 기본 Aggregate 객체 생성
        aggregate_name = action.args.get("aggregateName", f"Aggregate {action.ids.get('aggregateId', '')[:4]}")
        aggregate_alias = action.args.get("aggregateAlias", "")
        bounded_context_id = action.ids.get("boundedContextId", "")
        aggregate_id = action.ids.get("aggregateId", EsUtils.get_uuid())
        
        # Aggregate 객체 생성
        aggregate_object = AggregateProcessor._get_aggregate_base(
            user_info, aggregate_name, aggregate_alias, bounded_context_id, 0, 0, aggregate_id
        )
        
        # BoundedContext 레이아웃 조정
        AggregateProcessor._adjust_bounded_context_layout(es_value, action, aggregate_object)
        
        # 위치 설정
        valid_position = AggregateProcessor._get_valid_position(es_value, action, aggregate_object)
        aggregate_object["elementView"]["x"] = valid_position["x"]
        aggregate_object["elementView"]["y"] = valid_position["y"]
        
        # 속성 설정
        action.args["properties"] = AggregateProcessor._make_primary_key_property_if_not_exists(
            action.args.get("properties", [])
        )
        aggregate_object["aggregateRoot"]["fieldDescriptors"] = AggregateProcessor._get_field_descriptors(
            action.args.get("properties", [])
        )
        
        # es_value에 추가
        if "elements" not in es_value:
            es_value["elements"] = {}
        es_value["elements"][aggregate_object["id"]] = aggregate_object
        
        # Root Aggregate 객체 생성 및 추가
        root_aggregate_object = AggregateProcessor._get_root_aggregate_base(
            aggregate_name, 
            aggregate_id,
            AggregateProcessor._get_field_descriptors_for_root_aggregate(action.args.get("properties", []))
        )
        aggregate_object["aggregateRoot"]["entities"]["elements"][root_aggregate_object["id"]] = root_aggregate_object
    
    @staticmethod
    def _update_aggregate(action: Dict[str, Any], user_info: Dict[str, Any], 
                          information: Dict[str, Any], es_value: Dict[str, Any], 
                          callbacks: Dict[str, List]) -> None:
        """Aggregate 업데이트 액션을 처리합니다"""
        if action.args.get("properties"):
            aggregate_object = es_value["elements"].get(action.ids.get("aggregateId", ""), {})
            
            # Aggregate Root의 필드 업데이트
            if "aggregateRoot" in aggregate_object and "fieldDescriptors" in aggregate_object["aggregateRoot"]:
                aggregate_object["aggregateRoot"]["fieldDescriptors"] = AggregateProcessor._merge_field_descriptors(
                    aggregate_object["aggregateRoot"]["fieldDescriptors"],
                    action.args.get("properties", [])
                )
            
            # Root Aggregate 객체의 필드 업데이트
            root_aggregate_object = EsUtils.get_aggregate_root_object(aggregate_object)
            if root_aggregate_object:
                root_aggregate_object["fieldDescriptors"] = AggregateProcessor._merge_field_descriptors(
                    root_aggregate_object["fieldDescriptors"],
                    action.args.get("properties", [])
                )
            
            # 업데이트된 객체를 es_value에 저장
            es_value["elements"][action.ids.get("aggregateId", "")] = aggregate_object
    
    @staticmethod
    def _get_aggregate_base(user_info: Dict[str, Any], name: str, display_name: str, 
                           bounded_context_id: str, x: int, y: int, element_uuid: str) -> Dict[str, Any]:
        """Aggregate 기본 객체를 생성합니다"""
        element_uuid_to_use = element_uuid or EsUtils.get_uuid()
        
        return {
            "aggregateRoot": {
                "_type": "org.uengine.modeling.model.AggregateRoot",
                "fieldDescriptors": [],
                "entities": {
                    "elements": {},
                    "relations": {}
                },
                "operations": [],
            },
            "author": user_info.get("uid", ""),
            "boundedContext": {
                "name": bounded_context_id,
                "id": bounded_context_id
            },
            "commands": [],
            "description": None,
            "id": element_uuid_to_use,
            "elementView": {
                "_type": "org.uengine.modeling.model.Aggregate",
                "id": element_uuid_to_use,
                "x": x,
                "y": y,
                "width": 130,
                "height": 400,
            },
            "events": [],
            "hexagonalView": {
                "_type": "org.uengine.modeling.model.AggregateHexagonal",
                "id": element_uuid_to_use,
                "x": 0,
                "y": 0,
                "subWidth": 0,
                "width": 0,
            },
            "name": name,
            "displayName": display_name,
            "nameCamelCase": CaseConvertUtil.camel_case(name),
            "namePascalCase": CaseConvertUtil.pascal_case(name),
            "namePlural": CaseConvertUtil.plural(name),
            "rotateStatus": False,
            "selected": False,
            "_type": "org.uengine.modeling.model.Aggregate"
        }
    
    @staticmethod
    def _get_root_aggregate_base(name: str, aggregate_id: str, field_descriptors: List[Dict[str, Any]], element_uuid: str = None) -> Dict[str, Any]:
        """Root Aggregate 객체를 생성합니다"""
        element_uuid_to_use = element_uuid or EsUtils.get_uuid()
        
        return {
            "_type": "org.uengine.uml.model.Class",
            "id": element_uuid_to_use,
            "name": name,
            "namePascalCase": CaseConvertUtil.pascal_case(name),
            "nameCamelCase": CaseConvertUtil.camel_case(name),
            "namePlural": CaseConvertUtil.plural(name),
            "fieldDescriptors": field_descriptors,
            "operations": [],
            "elementView": {
                "_type": "org.uengine.uml.model.Class",
                "id": element_uuid_to_use,
                "x": 200,
                "y": 200,
                "width": 200,
                "height": 100,
                "style": "{}",
                "titleH": 50,
                "subEdgeH": 120,
                "fieldH": 90,
                "methodH": 30
            },
            "selected": False,
            "relations": [],
            "parentOperations": [],
            "relationType": None,
            "isVO": False,
            "isAbstract": False,
            "isInterface": False,
            "isAggregateRoot": True,
            "parentId": aggregate_id
        }
    
    @staticmethod
    def _get_valid_position(es_value: Dict[str, Any], action: Dict[str, Any], aggregate_object: Dict[str, Any]) -> Dict[str, int]:
        """Aggregate의 적절한 위치를 계산합니다"""
        bounded_context_id = action.ids.get("boundedContextId", "")
        aggregates = EsUtils.get_all_aggregates_in_bounded_context(es_value, bounded_context_id)
        
        if not aggregates:
            current_bounded_context = es_value["elements"].get(bounded_context_id, {})
            return {
                "x": current_bounded_context.get("elementView", {}).get("x", 0),
                "y": current_bounded_context.get("elementView", {}).get("y", 0)
            }
        else:
            max_x = max(agg["elementView"]["x"] for agg in aggregates)
            min_y = min(agg["elementView"]["y"] for agg in aggregates)
            
            max_x_aggregate = next(agg for agg in aggregates if agg["elementView"]["x"] == max_x)
            
            return {
                "x": max_x + max_x_aggregate["elementView"]["width"]//2 + aggregate_object["elementView"]["width"]//2 + 300,
                "y": min_y
            }
    
    @staticmethod
    def _adjust_bounded_context_layout(es_value: Dict[str, Any], action: Dict[str, Any], aggregate_object: Dict[str, Any]) -> None:
        """BoundedContext 레이아웃을 조정합니다"""
        MIN_CONTEXT_HEIGHT = 590
        MIN_CONTEXT_WIDTH = 560
        AGGREGATE_SPACING = 450
        
        bounded_context_id = action.ids.get("boundedContextId", "")
        target_bounded_context = es_value["elements"].get(bounded_context_id, {})
        
        # BoundedContext의 크기가 최소 크기보다 작으면 크기 조정
        if (target_bounded_context.get("elementView", {}).get("height", 0) < MIN_CONTEXT_HEIGHT or 
            target_bounded_context.get("elementView", {}).get("width", 0) < MIN_CONTEXT_WIDTH):
            
            height_delta = MIN_CONTEXT_HEIGHT - target_bounded_context.get("elementView", {}).get("height", 0)
            width_delta = MIN_CONTEXT_WIDTH - target_bounded_context.get("elementView", {}).get("width", 0)
            
            # BoundedContext 크기 업데이트
            target_bounded_context["elementView"]["height"] = target_bounded_context["elementView"].get("height", 0) + height_delta
            target_bounded_context["elementView"]["width"] = target_bounded_context["elementView"].get("width", 0) + width_delta
            target_bounded_context["elementView"]["y"] = target_bounded_context["elementView"].get("y", 0) + height_delta//2
            target_bounded_context["elementView"]["x"] = target_bounded_context["elementView"].get("x", 0) + width_delta//2
            
            es_value["elements"][bounded_context_id] = target_bounded_context
            
            # 인접 BoundedContext 이동
            AggregateProcessor._shift_adjacent_bounded_contexts(es_value, target_bounded_context, width_delta, height_delta)
        
        # Aggregate 목록 업데이트
        if "aggregates" not in target_bounded_context:
            target_bounded_context["aggregates"] = []
        target_bounded_context["aggregates"].append({"id": aggregate_object["id"]})


        # 이 BoundedContext에 있는 Aggregate가 없으면 종료
        aggregates = EsUtils.get_all_aggregates_in_bounded_context(es_value, bounded_context_id)
        if not aggregates:
            return


        # 인접 BoundedContext 이동
        AggregateProcessor._shift_adjacent_bounded_contexts(es_value, target_bounded_context, AGGREGATE_SPACING, 0)
        
        # BoundedContext 크기 업데이트
        target_bounded_context["elementView"]["x"] = target_bounded_context["elementView"].get("x", 0) + AGGREGATE_SPACING//2
        target_bounded_context["elementView"]["width"] = target_bounded_context["elementView"].get("width", 0) + AGGREGATE_SPACING
    
    @staticmethod
    def _shift_adjacent_bounded_contexts(es_value: Dict[str, Any], target_bounded_context: Dict[str, Any], offset_x: int, offset_y: int) -> None:
        """인접한 BoundedContext를 이동시킵니다"""
        for bounded_context_id in AggregateProcessor._find_right_side_bounded_context_ids(es_value, target_bounded_context):
            bounded_context = es_value["elements"].get(bounded_context_id, {})
            bounded_context["elementView"]["x"] = bounded_context["elementView"].get("x", 0) + offset_x
            es_value["elements"][bounded_context_id] = bounded_context
            
            # BoundedContext 내 요소들도 이동
            element_ids = [element["id"] for element in EsUtils.get_all_elements_in_bounded_context(es_value, bounded_context_id)]
            for element_id in element_ids:
                element = es_value["elements"].get(element_id, {})
                element["elementView"]["x"] = element["elementView"].get("x", 0) + offset_x
                es_value["elements"][element_id] = element
    
    @staticmethod
    def _find_right_side_bounded_context_ids(es_value: Dict[str, Any], target_bounded_context: Dict[str, Any]) -> List[str]:
        """대상 BoundedContext의 오른쪽에 있는 BoundedContext ID 목록을 반환합니다"""
        adjacent_context_ids = []
        for element_id, element in es_value["elements"].items():
            if (element and element.get("_type") == "org.uengine.modeling.model.BoundedContext" and 
                element["id"] != target_bounded_context["id"]):
                
                if ((target_bounded_context["elementView"]["x"] < element["elementView"]["x"]) and 
                    (target_bounded_context["elementView"]["y"] + target_bounded_context["elementView"]["height"]/2 > element["elementView"]["y"]) and
                    (target_bounded_context["elementView"]["y"] - target_bounded_context["elementView"]["height"]/2 < element["elementView"]["y"])):
                    adjacent_context_ids.append(element["id"])
        
        return adjacent_context_ids
    
    @staticmethod
    def _make_primary_key_property_if_not_exists(properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """기본 키가 없으면 기본 키 속성을 추가합니다"""
        if any(prop.get("isKey") for prop in properties):
            return properties
        return [{"name": "id", "type": "Long", "isKey": True}] + properties
    
    @staticmethod
    def _get_field_descriptors(properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Aggregate 필드 기술자를 생성합니다"""
        return [
            {
                "className": prop.get("type", "String"),
                "isCopy": False,
                "isKey": prop.get("isKey", False),
                "name": prop.get("name", ""),
                "nameCamelCase": CaseConvertUtil.camel_case(prop.get("name", "")),
                "namePascalCase": CaseConvertUtil.pascal_case(prop.get("name", "")),
                "displayName": prop.get("displayName", ""),
                "referenceClass": prop.get("referenceClass", None),
                "isOverrideField": prop.get("isOverrideField", False),
                "_type": "org.uengine.model.FieldDescriptor"
            }
            for prop in properties
        ]
    
    @staticmethod
    def _get_field_descriptors_for_root_aggregate(properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Root Aggregate 필드 기술자를 생성합니다"""
        return [
            {
                "className": prop.get("type", "String"),
                "isCopy": False,
                "isKey": prop.get("isKey", False),
                "name": prop.get("name", ""),
                "displayName": "",
                "nameCamelCase": CaseConvertUtil.camel_case(prop.get("name", "")),
                "namePascalCase": CaseConvertUtil.pascal_case(prop.get("name", "")),
                "_type": "org.uengine.model.FieldDescriptor",
                "inputUI": None,
                "options": None
            }
            for prop in properties
        ]
    
    @staticmethod
    def _merge_field_descriptors(existing_fields: List[Dict[str, Any]], new_properties: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """기존 필드와 새 속성을 병합합니다"""
        merged = existing_fields.copy()
        
        for new_prop in new_properties:
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
                merged.append(AggregateProcessor._get_field_descriptors([new_prop])[0])
        
        return merged