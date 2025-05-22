from typing import Any, Dict, List
import re

from ..models import ActionModel
from .vo_definitions import VODefinitions

class EsRestoreActionsUtil:
    @staticmethod
    def restoreActions(actions: List[ActionModel], esValue: Dict[str, Any]) -> None:
        """
        액션 목록을 검증하고 필요한 수정 작업을 수행합니다.
        
        Args:
            actions: 처리할 액션 목록
            esValue: 이벤트 스토밍 모델 데이터
        """
        EsRestoreActionsUtil._restoreDefaultPropertyType(actions)
        EsRestoreActionsUtil._restoreObjectTypeProperty(actions)
        EsRestoreActionsUtil._restoreTypeProperty(actions, esValue)
        EsRestoreActionsUtil._addDefaultValueObjectIfNotExists(actions, esValue)
        EsRestoreActionsUtil._changeInvalidMethodInExtendVerbURI(actions)

        EsRestoreActionsUtil._removeDuplicateAggregateInnerCreateActions(actions, esValue)
        EsRestoreActionsUtil._removeAggregateNameProperty(actions, esValue)
        EsRestoreActionsUtil._removeAggregateNameCreateAction(actions, esValue)
        EsRestoreActionsUtil._addAggregateInnerEntityIfAlreadyExists(actions, esValue)
        EsRestoreActionsUtil._addPropertyToAggregateRootIfNotExists(actions)
        EsRestoreActionsUtil._removeUselessValueObject(actions)
        EsRestoreActionsUtil._removeInvalidPropertiesInAggregateAttachments(actions, esValue)

    @staticmethod
    def _restoreDefaultPropertyType(actions: List[ActionModel]) -> None:
        """속성의 타입이 지정되지 않은 경우 기본값을 설정합니다."""
        for action in actions:
            if not hasattr(action, "args") or not hasattr(action.args, "properties"):
                continue
            
            if action.args.properties:
                for prop in action.args.properties:
                    if not hasattr(prop, "type") or not prop.type:
                        prop.type = "String"

    @staticmethod
    def _restoreTypeProperty(actions: List[ActionModel], esValue: Dict[str, Any]) -> None:
        """액션의 type 속성이 없는 경우 create 또는 update로 설정합니다."""
        for action in actions:
            if not hasattr(action, "type") or not action.type:
                id_to_search = None
                
                if action.objectType == "BoundedContext":
                    id_to_search = action.ids.get("boundedContextId")
                elif action.objectType == "Aggregate":
                    id_to_search = action.ids.get("aggregateId")
                elif action.objectType == "ValueObject":
                    id_to_search = action.ids.get("valueObjectId")
                elif action.objectType == "Enumeration":
                    id_to_search = action.ids.get("enumerationId")
                elif action.objectType == "Event":
                    id_to_search = action.ids.get("eventId")
                elif action.objectType == "Command":
                    id_to_search = action.ids.get("commandId")
                elif action.objectType == "GeneralClass":
                    id_to_search = action.ids.get("generalClassId")
                elif action.objectType == "ReadModel":
                    id_to_search = action.ids.get("readModelId")
                
                if not id_to_search:
                    action.type = "create"
                elif "elements" in esValue and id_to_search in esValue["elements"]:
                    action.type = "update"
                else:
                    action.type = "create"

    @staticmethod
    def _restoreObjectTypeProperty(actions: List[ActionModel]) -> None:
        """Entity와 GeneralClass가 혼동된 경우 복구합니다."""
        for action in actions:
            if action.objectType == "Entity":
                action.objectType = "GeneralClass"
                if hasattr(action, "args"):
                    if hasattr(action.args, "entityName"):
                        action.args.generalClassName = action.args.entityName
                    if hasattr(action.args, "entityAlias"):
                        action.args.generalClassAlias = action.args.entityAlias

    @staticmethod
    def _addDefaultValueObjectIfNotExists(actions: List[ActionModel], esValue: Dict[str, Any]) -> None:
        """필요한 ValueObject가 없는 경우 추가합니다."""
        VALID_OBJECT_TYPES = ['Aggregate', 'ValueObject', 'GeneralClass']
        vo_actions_to_add = []
        
        for action in actions:
            if action.objectType not in VALID_OBJECT_TYPES:
                continue
                
            # 이미 존재하는 VO 타입 수집
            existing_vo_types = set()
            
            for existing_action in actions + vo_actions_to_add:
                if (existing_action.objectType == 'ValueObject' and 
                    existing_action.type == 'create' and
                    existing_action.ids.get("aggregateId") == action.ids.get("aggregateId") and
                    hasattr(existing_action.args, "valueObjectName") and
                    existing_action.args.valueObjectName):
                    existing_vo_types.add(existing_action.args.valueObjectName)
            
            # esValue에서 이미 존재하는 엔티티 확인
            aggregate_id = action.ids.get("aggregateId")
            if esValue and "elements" in esValue and aggregate_id and aggregate_id in esValue["elements"]:
                aggregate_obj = esValue["elements"][aggregate_id]
                if (aggregate_obj and "aggregateRoot" in aggregate_obj and 
                    "entities" in aggregate_obj["aggregateRoot"] and 
                    "elements" in aggregate_obj["aggregateRoot"]["entities"]):
                    
                    for element in aggregate_obj["aggregateRoot"]["entities"]["elements"].values():
                        if element and "name" in element:
                            existing_vo_types.add(element["name"])
            
            # 필요한 VO 타입 식별
            required_vo_types = set()
            
            if hasattr(action, "args") and hasattr(action.args, "properties"):
                for prop in action.args.properties:
                    if not hasattr(prop, "type") or not prop.type:
                        continue
                        
                    pure_type = EsRestoreActionsUtil.__getPureType(prop.type)
                    if pure_type and pure_type in VODefinitions and pure_type not in existing_vo_types:
                        required_vo_types.add(pure_type)
            
            # 필요한 VO 액션 생성
            for vo_type in required_vo_types:
                vo_action = ActionModel(
                    objectType="ValueObject",
                    type="create",
                    ids={
                        "boundedContextId": action.ids.get("boundedContextId"),
                        "aggregateId": action.ids.get("aggregateId"),
                        "valueObjectId": f"vo-{vo_type.lower()}"
                    },
                    args={
                        "valueObjectName": vo_type,
                        "valueObjectAlias": "",
                        "properties": [{
                            "name": p.get("name"),
                            "type": p.get("className"),
                            "isKey": p.get("isKey", False)
                        } for p in VODefinitions[vo_type]]
                    }
                )
                vo_actions_to_add.append(vo_action)
                existing_vo_types.add(vo_type)
        
        actions.extend(vo_actions_to_add)

    @staticmethod
    def _changeInvalidMethodInExtendVerbURI(actions: List[ActionModel]) -> None:
        """PATCH 메서드를 PUT으로 변경합니다."""
        for action in actions:
            if (action.objectType == "Command" and 
                hasattr(action.args, "isRestRepository") and not action.args.isRestRepository and
                hasattr(action.args, "api_verb") and action.args.api_verb == "PATCH"):
                action.args.api_verb = "PUT"

    @staticmethod
    def _removeDuplicateAggregateInnerCreateActions(actions: List[ActionModel], esValue: Dict[str, Any]) -> None:
        """동일한 Aggregate 내에서 중복된 이름의 ValueObject, Enumeration, GeneralClass 생성 액션을 제거합니다."""
        if not actions or not esValue or "elements" not in esValue:
            return
            
        # Aggregate별 기존 엔티티 이름 수집
        aggregate_element_names = {}
        
        for action in actions:
            aggregate_id = action.ids.get("aggregateId")
            if not aggregate_id or aggregate_id in aggregate_element_names:
                continue
                
            names = set()
            if (aggregate_id in esValue["elements"] and 
                "aggregateRoot" in esValue["elements"][aggregate_id] and 
                "entities" in esValue["elements"][aggregate_id]["aggregateRoot"] and 
                "elements" in esValue["elements"][aggregate_id]["aggregateRoot"]["entities"]):
                
                for element in esValue["elements"][aggregate_id]["aggregateRoot"]["entities"]["elements"].values():
                    if element and "name" in element:
                        names.add(element["name"].lower())
                        
            aggregate_element_names[aggregate_id] = names
        
        # 액션에서 이름 추출 함수
        def get_name_from_action(action):
            if action.objectType == 'ValueObject' and hasattr(action.args, 'valueObjectName'):
                return action.args.valueObjectName
            elif action.objectType == 'Enumeration' and hasattr(action.args, 'enumerationName'):
                return action.args.enumerationName
            elif action.objectType == 'GeneralClass' and hasattr(action.args, 'generalClassName'):
                return action.args.generalClassName
            return None
        
        # 이미 사용된 이름 추적
        used_names = {}
        
        # 중복 액션 필터링
        filtered_actions = []
        for action in actions:
            if action.type != 'create' or action.objectType not in ["ValueObject", "Enumeration", "GeneralClass"]:
                filtered_actions.append(action)
                continue
                
            name = get_name_from_action(action)
            if not name:
                filtered_actions.append(action)
                continue
                
            aggregate_id = action.ids.get("aggregateId")
            if not aggregate_id:
                filtered_actions.append(action)
                continue
                
            if aggregate_id not in used_names:
                used_names[aggregate_id] = set()
                
            used_names_in_aggregate = used_names[aggregate_id]
            existing_names_in_aggregate = aggregate_element_names.get(aggregate_id, set())
            
            # 중복 이름이 아닌 경우만 추가
            if ((name.lower() not in existing_names_in_aggregate) and 
                (name.lower() not in used_names_in_aggregate)):
                filtered_actions.append(action)
                used_names_in_aggregate.add(name.lower())
        
        # 원본 actions 리스트 교체
        actions.clear()
        actions.extend(filtered_actions)

    @staticmethod
    def _removeAggregateNameProperty(actions: List[ActionModel], esValue: Dict[str, Any]) -> None:
        """Aggregate 이름을 직접적으로 속성으로 가지는 경우 제거합니다."""
        # Aggregate 이름 수집
        aggregate_names = set()
        for element in esValue["elements"].values():
            if element and element.get("_type") == "org.uengine.modeling.model.Aggregate":
                aggregate_names.add(element.get("name"))
        
        # 속성 필터링
        for action in actions:
            if hasattr(action, "args") and hasattr(action.args, "properties"):
                filtered_properties = []
                
                for prop in action.args.properties:
                    # 속성 타입이 Aggregate 이름인 경우 제외
                    is_not_aggregate_type = not hasattr(prop, "type") or prop.type not in aggregate_names
                    
                    # Aggregate Id 속성 확인
                    is_aggregate_id_property = False
                    if not (hasattr(action.args, "valueObjectName") and 
                           action.args.valueObjectName and 
                           action.args.valueObjectName.lower().endswith("id")):
                        for agg_name in aggregate_names:
                            if (hasattr(prop, "name") and 
                                prop.name and 
                                prop.name.lower() == (agg_name.lower() + "id") and
                                EsRestoreActionsUtil.__isDefaultJavaType(prop.type)):
                                is_aggregate_id_property = True
                                break
                    
                    if is_not_aggregate_type and not is_aggregate_id_property:
                        filtered_properties.append(prop)
                
                action.args.properties = filtered_properties

    @staticmethod
    def _removeAggregateNameCreateAction(actions: List[ActionModel], esValue: Dict[str, Any]) -> None:
        """Aggregate 이름과 동일한 이름의 ValueObject, GeneralClass 생성 액션을 제거합니다."""
        # Aggregate 이름 수집
        aggregate_names = set()
        for element in esValue["elements"].values():
            if element and element.get("_type") == "org.uengine.modeling.model.Aggregate":
                aggregate_names.add(element.get("name"))
        
        # 액션 필터링
        filtered_actions = []
        for action in actions:
            if action.type != 'create' or action.objectType not in ["ValueObject", "GeneralClass"]:
                filtered_actions.append(action)
                continue
                
            name = None
            if action.objectType == "ValueObject" and hasattr(action.args, "valueObjectName"):
                name = action.args.valueObjectName
            elif action.objectType == "GeneralClass" and hasattr(action.args, "generalClassName"):
                name = action.args.generalClassName
                
            if not name or name not in aggregate_names:
                filtered_actions.append(action)
        
        # 원본 actions 리스트 교체
        actions.clear()
        actions.extend(filtered_actions)

    @staticmethod
    def _addAggregateInnerEntityIfAlreadyExists(actions: List[ActionModel], esValue: Dict[str, Any]) -> None:
        """다른 Aggregate에 있는 타입을 현재 Aggregate에 복사합니다."""
        VALID_OBJECT_TYPES = ['Aggregate', 'ValueObject', 'GeneralClass']
        actions_to_add = []
        
        for action in actions:
            if action.objectType not in VALID_OBJECT_TYPES or action.type != 'create':
                continue
                
            new_actions = EsRestoreActionsUtil._createNewActionsForMissingTypes(action, actions, esValue)
            actions_to_add.extend(new_actions)
        
        if not actions_to_add:
            return
            
        unique_actions = EsRestoreActionsUtil._filterAndAddUniqueActions(actions, actions_to_add)
        actions.extend(unique_actions)

    @staticmethod
    def _createNewActionsForMissingTypes(action: ActionModel, actions: List[ActionModel], esValue: Dict[str, Any]) -> List[ActionModel]:
        """누락된 타입에 대한 새 액션을 생성합니다."""
        new_actions = []
        properties = getattr(action.args, "properties", []) or []
        properties_to_remove = []
        
        for i, prop in enumerate(properties):
            if not hasattr(prop, "type") or not prop.type:
                continue
                
            pure_type = EsRestoreActionsUtil.__getPureType(prop.type)
            if EsRestoreActionsUtil.__isDefaultJavaType(pure_type):
                continue
                
            if EsRestoreActionsUtil._isTypeExistsInActionsOrAggregate(pure_type, action, actions, esValue):
                continue
                
            found = EsRestoreActionsUtil._findTypeInAggregates(
                esValue,
                pure_type,
                getattr(prop, "referenceClass", None)
            )
            
            if found:
                new_action = EsRestoreActionsUtil._createActionFromFoundType(found, action)
                new_actions.append(new_action)
            else:
                properties_to_remove.append(i)
        
        # 속성 제거 (뒤에서부터 제거해야 인덱스가 변하지 않음)
        for i in sorted(properties_to_remove, reverse=True):
            properties.pop(i)
        
        return new_actions

    @staticmethod
    def _findTypeInAggregates(esValue: Dict[str, Any], type_name: str, reference_aggregate_id: str = None) -> Dict[str, Any]:
        """다른 Aggregate에서 지정된 타입을 찾습니다."""
        # 참조된 Aggregate에서 먼저 검색
        if (reference_aggregate_id and esValue and "elements" in esValue and 
            reference_aggregate_id in esValue["elements"]):
            aggregate = esValue["elements"][reference_aggregate_id]
            if (aggregate and "aggregateRoot" in aggregate and 
                "entities" in aggregate["aggregateRoot"] and 
                "elements" in aggregate["aggregateRoot"]["entities"]):
                
                for element in aggregate["aggregateRoot"]["entities"]["elements"].values():
                    if element and element.get("name") == type_name:
                        return {"element": element, "aggregateId": reference_aggregate_id}
        
        # 모든 Aggregate에서 검색
        for element_id, element in esValue["elements"].items():
            if (element and element.get("_type") == "org.uengine.modeling.model.Aggregate" and
                "aggregateRoot" in element and 
                "entities" in element["aggregateRoot"] and
                "elements" in element["aggregateRoot"]["entities"]):
                
                for entity in element["aggregateRoot"]["entities"]["elements"].values():
                    if entity and entity.get("name") == type_name:
                        return {"element": entity, "aggregateId": element_id}
        
        return None

    @staticmethod
    def _createActionFromFoundType(found: Dict[str, Any], original_action: ActionModel) -> ActionModel:
        """찾은 타입을 기반으로 새 액션을 생성합니다."""
        element = found["element"]
        
        new_action = ActionModel(
            ids={
                "boundedContextId": original_action.ids.get("boundedContextId"),
                "aggregateId": original_action.ids.get("aggregateId"),
            },
            args={
                "properties": []
            }
        )
        
        # 필드 추가
        if "fieldDescriptors" in element:
            new_action.args.properties = [
                {
                    "name": fd.get("name"),
                    "type": fd.get("className"),
                    "isKey": fd.get("isKey", False)
                }
                for fd in element["fieldDescriptors"]
            ]
        
        # 타입에 따른 추가 속성 설정
        if element.get("_type") == "org.uengine.uml.model.vo.Class":
            new_action.objectType = "ValueObject"
            new_action.ids["valueObjectId"] = f"vo-{element['name'].lower()}"
            new_action.args.valueObjectName = element["name"]
            new_action.args.valueObjectAlias = element.get("displayName", "")
        elif element.get("_type") == "org.uengine.uml.model.Class":
            new_action.objectType = "GeneralClass"
            new_action.ids["generalClassId"] = f"gc-{element['name'].lower()}"
            new_action.args.generalClassName = element["name"]
            new_action.args.generalClassAlias = element.get("displayName", "")
        elif element.get("_type") == "org.uengine.uml.model.enum":
            new_action.objectType = "Enumeration"
            new_action.ids["enumerationId"] = f"enum-{element['name'].lower()}"
            new_action.args.enumerationName = element["name"]
            new_action.args.enumerationAlias = element.get("displayName", "")
            new_action.args.properties = [{"name": item["value"]} for item in element.get("items", [])]
        
        new_action.type = "create"
        return new_action

    @staticmethod
    def _filterAndAddUniqueActions(existing_actions: List[ActionModel], new_actions: List[ActionModel]) -> List[ActionModel]:
        """중복되지 않는 액션만 추가합니다."""
        def get_action_key(action):
            name = None
            if action.objectType == 'ValueObject' and hasattr(action.args, "valueObjectName"):
                name = action.args.valueObjectName
            elif action.objectType == 'GeneralClass' and hasattr(action.args, "generalClassName"):
                name = action.args.generalClassName
            elif action.objectType == 'Enumeration' and hasattr(action.args, "enumerationName"):
                name = action.args.enumerationName
            
            if not name:
                return None
                
            return f"{action.objectType}|{action.ids.get('aggregateId')}|{name}"
        
        # 기존 액션 키 수집
        existing_action_keys = set()
        for action in existing_actions:
            key = get_action_key(action)
            if key:
                existing_action_keys.add(key)
        
        # 중복되지 않는 액션만 필터링
        unique_actions = []
        for action in new_actions:
            key = get_action_key(action)
            if key and key not in existing_action_keys:
                unique_actions.append(action)
                existing_action_keys.add(key)
        
        return unique_actions

    @staticmethod
    def _addPropertyToAggregateRootIfNotExists(actions: List[ActionModel]) -> None:
        """GeneralClass, Entity, Enumeration이 생성되어 있지만 사용되지 않는 경우 AggregateRoot에 속성을 추가합니다."""
        # 대상 액션 필터링
        inner_actions = [
            action for action in actions
            if action.objectType in ["GeneralClass", "ValueObject", "Enumeration"] and
            action.type == "create"
        ]
        
        if not inner_actions:
            return
            
        # Aggregate 액션 매핑
        aggregate_map = {}
        for action in actions:
            if action.objectType == "Aggregate":
                aggregate_map[action.ids.get("aggregateId")] = action
        
        # 사용된 타입 수집
        used_types_by_aggregate = {}
        for action in actions:
            if hasattr(action, "args") and hasattr(action.args, "properties") and "aggregateId" in action.ids:
                aggregate_id = action.ids["aggregateId"]
                
                if aggregate_id not in used_types_by_aggregate:
                    used_types_by_aggregate[aggregate_id] = set()
                    
                used_types = used_types_by_aggregate[aggregate_id]
                
                for prop in action.args.properties:
                    if hasattr(prop, "type") and prop.type:
                        pure_type = EsRestoreActionsUtil.__getPureType(prop.type)
                        used_types.add(pure_type)
        
        # 필요한 속성 추가
        for action in inner_actions:
            aggregate_id = action.ids.get("aggregateId")
            if aggregate_id not in aggregate_map:
                continue
                
            aggregate_action = aggregate_map[aggregate_id]
            
            element_name = None
            if action.objectType == "GeneralClass" and hasattr(action.args, "generalClassName"):
                element_name = action.args.generalClassName
            elif action.objectType == "ValueObject" and hasattr(action.args, "valueObjectName"):
                element_name = action.args.valueObjectName
            elif action.objectType == "Enumeration" and hasattr(action.args, "enumerationName"):
                element_name = action.args.enumerationName
            
            if not element_name:
                continue
                
            # 해당 타입이 이미 사용되고 있는지 확인
            used_types_in_aggregate = used_types_by_aggregate.get(aggregate_id, set())
            if element_name in used_types_in_aggregate:
                continue
                
            # 속성 추가
            if not hasattr(aggregate_action.args, "properties"):
                aggregate_action.args.properties = []
                
            new_property = {
                "name": EsRestoreActionsUtil.__generatePropertyName(element_name),
                "type": element_name
            }
            
            # 중복 검사
            if not any(p.get("name") == new_property["name"] for p in aggregate_action.args.properties):
                aggregate_action.args.properties.append(new_property)

    @staticmethod
    def _removeUselessValueObject(actions: List[ActionModel]) -> None:
        """속성이 1개만 있는 ValueObject를 제거하고 해당 속성을 직접 사용하도록 변경합니다."""
        # 타입과 별칭 매핑
        type_alias_map = {}
        for action in actions:
            if action.objectType in ["Enumeration", "ValueObject", "Entity"]:
                object_type_lower = action.objectType.lower()
                name_attr = f"{object_type_lower}Name"
                alias_attr = f"{object_type_lower}Alias"
                
                if hasattr(action.args, name_attr) and hasattr(action.args, alias_attr):
                    name = getattr(action.args, name_attr)
                    alias = getattr(action.args, alias_attr)
                    if name and alias:
                        type_alias_map[name] = alias
        
        # 제거할 ValueObject 식별
        vo_to_remove = {}
        vo_actions = [
            action for action in actions
            if action.objectType == "ValueObject" and
            hasattr(action.args, "properties") and
            action.args.properties and
            len(action.args.properties) == 1 and
            not (hasattr(action.args, "valueObjectName") and 
                 action.args.valueObjectName.lower().endswith("id"))
        ]
        
        for action in vo_actions:
            vo_name = action.args.valueObjectName
            property = action.args.properties[0]
            vo_to_remove[vo_name] = {
                "type": property.type,
                "alias": action.args.valueObjectAlias
            }
        
        # 속성 타입 변경
        for action in actions:
            if hasattr(action, "args") and hasattr(action.args, "properties"):
                for prop in action.args.properties:
                    if not hasattr(prop, "type") or not prop.type:
                        continue
                        
                    pure_type = EsRestoreActionsUtil.__getPureType(prop.type)
                    if pure_type in vo_to_remove:
                        vo_info = vo_to_remove[pure_type]
                        new_pure_type = EsRestoreActionsUtil.__getPureType(vo_info["type"])
                        
                        prop.type = prop.type.replace(pure_type, vo_info["type"])
                        if not EsRestoreActionsUtil.__isDefaultJavaType(new_pure_type) and new_pure_type in type_alias_map:
                            prop.displayName = type_alias_map[new_pure_type]
        
        # 제거할 ValueObject 액션 필터링
        filtered_actions = [
            action for action in actions
            if not (action.objectType == "ValueObject" and
                  hasattr(action.args, "valueObjectName") and
                  action.args.valueObjectName in vo_to_remove)
        ]
        
        # 원본 actions 리스트 교체
        actions.clear()
        actions.extend(filtered_actions)

    @staticmethod
    def _removeInvalidPropertiesInAggregateAttachments(actions: List[ActionModel], esValue: Dict[str, Any]) -> None:
        """Command, Event, ReadModel에서 유효하지 않은 속성을 제거합니다."""
        ATTACHMENT_TYPES = ['Command', 'Event', 'ReadModel']
        
        for action in actions:
            if action.objectType not in ATTACHMENT_TYPES or action.type != 'create':
                continue
                
            EsRestoreActionsUtil._removeInvalidPropertiesInAggregateAttachmentsForAction(action, actions, esValue)

    @staticmethod
    def _removeInvalidPropertiesInAggregateAttachmentsForAction(action: ActionModel, actions: List[ActionModel], esValue: Dict[str, Any]) -> None:
        """특정 액션에서 유효하지 않은 속성을 제거합니다."""
        properties = []
        if hasattr(action.args, "properties") and action.args.properties:
            properties = action.args.properties
        elif hasattr(action.args, "queryParameters") and action.args.queryParameters:
            properties = action.args.queryParameters
        
        if not properties:
            return
            
        properties_to_remove = []
        
        for i, prop in enumerate(properties):
            if not hasattr(prop, "type") or not prop.type:
                continue
                
            pure_type = EsRestoreActionsUtil.__getPureType(prop.type)
            if EsRestoreActionsUtil.__isDefaultJavaType(pure_type):
                continue
                
            if EsRestoreActionsUtil._isTypeExistsInActionsOrAggregate(pure_type, action, actions, esValue):
                continue
                
            properties_to_remove.append(i)
        
        # 속성 제거 (뒤에서부터 제거해야 인덱스가 변하지 않음)
        for i in sorted(properties_to_remove, reverse=True):
            properties.pop(i)

    @staticmethod
    def _isTypeExistsInActionsOrAggregate(pure_type: str, action: ActionModel, actions: List[ActionModel], esValue: Dict[str, Any]) -> bool:
        """해당 타입이 액션 목록이나 Aggregate에 존재하는지 확인합니다."""
        # 액션 목록에서 확인
        for a in actions:
            if (a.type == 'create' and 
                a.ids.get("aggregateId") == action.ids.get("aggregateId")):
                
                if ((a.objectType == 'ValueObject' and hasattr(a.args, 'valueObjectName') and a.args.valueObjectName == pure_type) or
                    (a.objectType == 'GeneralClass' and hasattr(a.args, 'generalClassName') and a.args.generalClassName == pure_type) or
                    (a.objectType == 'Enumeration' and hasattr(a.args, 'enumerationName') and a.args.enumerationName == pure_type)):
                    return True
        
        # Aggregate에서 확인
        target_aggregate_id = action.ids.get("aggregateId")
        if target_aggregate_id and "elements" in esValue and target_aggregate_id in esValue["elements"]:
            target_aggregate = esValue["elements"][target_aggregate_id]
            
            if (target_aggregate and "aggregateRoot" in target_aggregate and
                "entities" in target_aggregate["aggregateRoot"] and
                "elements" in target_aggregate["aggregateRoot"]["entities"]):
                
                for element in target_aggregate["aggregateRoot"]["entities"]["elements"].values():
                    if element and element.get("name") == pure_type:
                        return True
        
        return False

    @staticmethod
    def __getPureType(type_str: str) -> str:
        """타입 문자열에서 순수한 타입 이름을 추출합니다."""
        match = re.search(r'<(.+)>', type_str)
        type_from_match = match.group(1) if match else type_str
        return type_from_match.replace("[]", "")

    @staticmethod
    def __isDefaultJavaType(type_str: str) -> bool:
        """자바 기본 타입인지 확인합니다."""
        default_types = [
            "String", "Integer", "Long", "Double", "Float", "Boolean", 
            "Date", "LocalDate", "LocalDateTime", "LocalTime", "Timestamp", 
            "BigDecimal", "BigInteger", "Byte", "Short", "Character", 
            "Enum", "Object"
        ]
        return type_str in default_types

    @staticmethod
    def __generatePropertyName(element_name: str) -> str:
        """요소 이름으로부터 속성 이름을 생성합니다."""
        return element_name[0].lower() + element_name[1:]