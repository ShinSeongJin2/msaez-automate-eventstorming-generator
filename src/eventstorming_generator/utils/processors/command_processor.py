from typing import Dict, Any, List

from ..convert_case_util import CaseConvertUtil
from ..es_utils import EsUtils

class CommandProcessor:
    @staticmethod
    def get_action_applied_es_value(action: Dict[str, Any], user_info: Dict[str, Any], 
                                   information: Dict[str, Any], es_value: Dict[str, Any], 
                                   callbacks: Dict[str, List]) -> None:
        """액션에 따라 Command를 처리합니다"""
        if action.type == "create":
            CommandProcessor._create_command(action, user_info, information, es_value, callbacks)
    
    @staticmethod
    def _create_command(action: Dict[str, Any], user_info: Dict[str, Any], 
                        information: Dict[str, Any], es_value: Dict[str, Any], 
                        callbacks: Dict[str, List]) -> None:
        """Command 생성 액션을 처리합니다"""
        command_name = action.args.get("commandName", "")
        command_alias = action.args.get("commandAlias", "")
        api_verb = action.args.get("api_verb", "")
        is_rest_repository = action.args.get("isRestRepository", False)
        bounded_context_id = action.ids.get("boundedContextId", "")
        aggregate_id = action.ids.get("aggregateId", "")
        command_id = action.ids.get("commandId", EsUtils.get_uuid())
        
        # Command 객체 생성
        command_object = CommandProcessor._get_command_base(
            user_info, command_name, command_alias, api_verb, [], is_rest_repository,
            bounded_context_id, aggregate_id, 0, 0, command_id
        )
        
        # 출력 이벤트 설정
        if action.args.get("outputEventIds"):
            def set_output_events(es_value: Dict[str, Any], user_info: Dict[str, Any], 
                                information: Dict[str, Any]) -> None:
                command_object["outputEvents"] = CommandProcessor._get_output_event_names(
                    es_value, action.args.get("outputEventIds", [])
                )
            callbacks["afterAllObjectAppliedCallBacks"].append(set_output_events)
        else:
            command_object["outputEvents"] = []
        
        # Command-Event 관계 설정
        CommandProcessor._make_command_to_event_relation(command_object, action, callbacks)
        
        # 위치 설정
        valid_position = CommandProcessor._get_valid_position(es_value, action, command_object)
        command_object["elementView"]["x"] = valid_position["x"]
        command_object["elementView"]["y"] = valid_position["y"]
        
        # Actor-Command 관계 설정
        def make_actor_to_command(es_value: Dict[str, Any], user_info: Dict[str, Any], 
                                information: Dict[str, Any]) -> None:
            from .actor_processor import ActorProcessor
            ActorProcessor.make_actor_to_command(es_value, action, command_object, user_info)
        callbacks["afterAllRelationAppliedCallBacks"].append(make_actor_to_command)
        
        # 필드 설정
        command_object["fieldDescriptors"] = CommandProcessor._get_field_descriptors(es_value, action)
        
        # Command 객체 추가
        es_value["elements"][command_object["id"]] = command_object
        
        # Aggregate 크기 조정
        EsUtils.resize_aggregate_vertically(es_value, command_object)
    
    @staticmethod
    def _get_command_base(user_info: Dict[str, Any], name: str, display_name: str, 
                         api_verb: str, output_events: List[str], is_rest_repository: bool, 
                         bounded_context_id: str, aggregate_id: str, x: int, y: int, 
                         element_uuid: str = None) -> Dict[str, Any]:
        """Command 기본 객체를 생성합니다"""
        element_uuid_to_use = element_uuid or EsUtils.get_uuid()
        
        return {
            "_type": "org.uengine.modeling.model.Command",
            "outputEvents": output_events,
            "aggregate": {
                "id": aggregate_id
            },
            "author": user_info.get("uid", ""),
            "boundedContext": {
                "id": bounded_context_id,
            },
            "controllerInfo": {
                "apiPath": name.lower(),
                "method": api_verb,
                "fullApiPath": ""
            },
            "fieldDescriptors": [],
            "description": None,
            "id": element_uuid_to_use,
            "elementView": {
                "_type": "org.uengine.modeling.model.Command",
                "height": 115,
                "id": element_uuid_to_use,
                "style": "{}",
                "width": 100,
                "x": x, 
                "y": y,
                "z-index": 999
            },
            "hexagonalView": {
                "_type": "org.uengine.modeling.model.CommandHexagonal",
                "height": 0,
                "id": element_uuid_to_use,
                "style": "{}",
                "width": 0,
                "x": 0,
                "y": 0
            },
            "isRestRepository": is_rest_repository,
            "name": name,
            "displayName": display_name,
            "nameCamelCase": CaseConvertUtil.camel_case(name),
            "namePascalCase": CaseConvertUtil.pascal_case(name),
            "namePlural": CaseConvertUtil.plural(name),
            "relationCommandInfo": [],
            "relationEventInfo": [],
            "restRepositoryInfo": {
                "method": api_verb if api_verb else 'POST'
            },
            "rotateStatus": False,
            "selected": False,
            "trigger": "@PrePersist",
        }
    
    @staticmethod
    def _get_output_event_names(es_value: Dict[str, Any], output_event_ids: List[str]) -> List[str]:
        """출력 이벤트 ID에서 이벤트 이름 목록을 가져옵니다"""
        return [
            es_value["elements"][event_id]["name"]
            for event_id in output_event_ids
            if es_value["elements"].get(event_id)
        ]
    
    @staticmethod
    def _make_command_to_event_relation(command_object: Dict[str, Any], 
                                       action: Dict[str, Any], 
                                       callbacks: Dict[str, List]) -> None:
        """Command와 Event 간의 관계를 생성합니다"""
        def create_relations(es_value: Dict[str, Any], user_info: Dict[str, Any], 
                            information: Dict[str, Any]) -> None:
            if not action.args.get("outputEventIds") or len(action.args.get("outputEventIds", [])) <= 0:
                return
                
            for event_id in action.args.get("outputEventIds", []):
                event_object = es_value["elements"].get(event_id)
                if not command_object or not event_object:
                    continue
                    
                command_event_relation = EsUtils.getEventStormingRelationObjectBase(command_object, event_object)
                es_value["relations"][command_event_relation["id"]] = command_event_relation
        
        callbacks["afterAllObjectAppliedCallBacks"].append(create_relations)
    
    @staticmethod
    def _get_valid_position(es_value: Dict[str, Any], action: Dict[str, Any], 
                           command_object: Dict[str, Any]) -> Dict[str, int]:
        """Command의 적절한 위치를 계산합니다"""
        aggregate_id = action.ids.get("aggregateId", "")
        commands = EsUtils.get_aggregate_commands(es_value, aggregate_id)
        read_models = EsUtils.get_aggregate_read_models(es_value, aggregate_id)
        all_models = commands + read_models
        
        if len(all_models) <= 0:
            current_aggregate = es_value["elements"].get(aggregate_id, {})
            if not current_aggregate:
                return {"x": 0, "y": 0}
                
            return {
                "x": current_aggregate["elementView"]["x"] - int(current_aggregate["elementView"]["width"]/2) - 29,
                "y": current_aggregate["elementView"]["y"] - int(current_aggregate["elementView"]["height"]/2)
            }
        else:
            min_x = min(model["elementView"]["x"] for model in all_models)
            max_y = max(model["elementView"]["y"] for model in all_models)
            
            max_y_models = [model for model in all_models if model["elementView"]["y"] == max_y]
            if not max_y_models:
                return {"x": min_x, "y": max_y + 150}
                
            max_y_model = max_y_models[0]
            return {
                "x": min_x,
                "y": max_y + int(max_y_model["elementView"]["height"]/2) + int(command_object["elementView"]["height"]/2) + 14
            }
    
    @staticmethod
    def _get_field_descriptors(es_value: Dict[str, Any], action: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Command의 필드 디스크립터를 생성합니다"""
        if action.args.get("properties"):
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
                for prop in action.args.get("properties", [])
            ]
        
        aggregate = es_value["elements"].get(action.ids.get("aggregateId", ""), {})
        if not aggregate or not aggregate.get("aggregateRoot") or not aggregate["aggregateRoot"].get("fieldDescriptors"):
            return []
            
        target_field_descriptors = aggregate["aggregateRoot"]["fieldDescriptors"]
        if action.args.get("api_verb") == "DELETE":
            target_field_descriptors = [fd for fd in target_field_descriptors if fd.get("isKey")]
        
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