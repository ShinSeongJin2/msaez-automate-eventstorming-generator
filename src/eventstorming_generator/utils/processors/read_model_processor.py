from typing import Dict, Any, List
from convert_case import camel_case, pascal_case
from pluralizer import Pluralizer

from ..es_utils import EsUtils

pluralizer = Pluralizer()
class ReadModelProcessor:
    @staticmethod
    def get_action_applied_es_value(action: Dict[str, Any], user_info: Dict[str, Any], 
                                   information: Dict[str, Any], es_value: Dict[str, Any], 
                                   callbacks: Dict[str, List]) -> None:
        """액션에 따라 ReadModel를 처리합니다"""
        if action["type"] == "create":
            ReadModelProcessor._create_read_model(action, user_info, information, es_value, callbacks)
    
    @staticmethod
    def _create_read_model(action: Dict[str, Any], user_info: Dict[str, Any], 
                         information: Dict[str, Any], es_value: Dict[str, Any], 
                         callbacks: Dict[str, List]) -> None:
        """ReadModel 생성 액션을 처리합니다"""
        read_model_name = action["args"].get("readModelName", "")
        read_model_alias = action["args"].get("readModelAlias", "")
        is_multiple_result = action["args"].get("isMultipleResult", False)
        bounded_context_id = action["ids"].get("boundedContextId", "")
        aggregate_id = action["ids"].get("aggregateId", "")
        read_model_id = action["ids"].get("readModelId", EsUtils.get_uuid())
        
        # ReadModel 객체 생성
        read_model_object = ReadModelProcessor._get_read_model_base(
            user_info, read_model_name, read_model_alias, is_multiple_result,
            bounded_context_id, aggregate_id, 0, 0, read_model_id
        )
        
        # 위치 설정
        valid_position = ReadModelProcessor._get_valid_position(es_value, action, read_model_object)
        read_model_object["elementView"]["x"] = valid_position["x"]
        read_model_object["elementView"]["y"] = valid_position["y"]
        
        # Actor-ReadModel 관계 설정
        def make_actor_to_read_model(es_value: Dict[str, Any], user_info: Dict[str, Any], 
                                   information: Dict[str, Any]) -> None:
            from .actor_processor import ActorProcessor
            ActorProcessor.make_actor_to_command(es_value, action, read_model_object, user_info)
        callbacks["afterAllRelationAppliedCallBacks"].append(make_actor_to_read_model)
        
        # 쿼리 파라미터 설정
        read_model_object["queryParameters"] = ReadModelProcessor._get_query_parameters(es_value, action)
        
        # ReadModel 객체 추가
        es_value["elements"][read_model_object["id"]] = read_model_object
        
        # Aggregate 크기 조정
        EsUtils.resize_aggregate_vertically(es_value, read_model_object)
    
    @staticmethod
    def _get_read_model_base(user_info: Dict[str, Any], name: str, display_name: str, 
                           is_multiple_result: bool, bounded_context_id: str, 
                           aggregate_id: str, x: int, y: int, 
                           element_uuid: str = None) -> Dict[str, Any]:
        """ReadModel 기본 객체를 생성합니다"""
        element_uuid_to_use = element_uuid or EsUtils.get_uuid()
        
        return {
            "_type": "org.uengine.modeling.model.View",
            "id": element_uuid_to_use,
            "visibility": "public",
            "name": name,
            "oldName": "",
            "displayName": display_name,
            "namePascalCase": pascal_case(name),
            "namePlural": pluralizer.plural(camel_case(name)),
            "aggregate": {
                "id": aggregate_id
            },
            "description": None,
            "author": user_info.get("uid", ""),
            "boundedContext": {
                "id": bounded_context_id
            },
            "fieldDescriptors": [
                {
                    "_type": "org.uengine.model.FieldDescriptor",
                    "name": "id",
                    "className": "Long",
                    "nameCamelCase": "id",
                    "namePascalCase": "Id",
                    "isKey": True
                }
            ],
            "queryParameters": [],
            "queryOption": {
                "apiPath": "",
                "useDefaultUri": True,
                "multipleResult": is_multiple_result
            },
            "controllerInfo": {
                "url": ""
            },
            "elementView": {
                "_type": "org.uengine.modeling.model.View",
                "id": element_uuid_to_use,
                "x": x,
                "y": y,
                "width": 100,
                "height": 115,
                "style": "{}",
                "z-index": 999
            },
            "editingView": False,
            "dataProjection": "query-for-aggregate",
            "createRules": [
                {
                    "_type": "viewStoreRule",
                    "operation": "CREATE",
                    "when": None,
                    "fieldMapping": [
                        {
                            "viewField": None,
                            "eventField": None,
                            "operator": "="
                        }
                    ],
                    "where": [
                        {
                            "viewField": None,
                            "eventField": None
                        }
                    ]
                }
            ],
            "updateRules": [
                {
                    "_type": "viewStoreRule",
                    "operation": "UPDATE",
                    "when": None,
                    "fieldMapping": [
                        {
                            "viewField": None,
                            "eventField": None,
                            "operator": "="
                        }
                    ],
                    "where": [
                        {
                            "viewField": None,
                            "eventField": None
                        }
                    ]
                }
            ],
            "deleteRules": [
                {
                    "_type": "viewStoreRule",
                    "operation": "DELETE",
                    "when": None,
                    "fieldMapping": [
                        {
                            "viewField": None,
                            "eventField": None
                        }
                    ],
                    "where": [
                        {
                            "viewField": None,
                            "eventField": None
                        }
                    ]
                }
            ],
            "rotateStatus": False,
            "definitionId": ""
        }
    
    @staticmethod
    def _get_valid_position(es_value: Dict[str, Any], action: Dict[str, Any], 
                          read_model_object: Dict[str, Any]) -> Dict[str, int]:
        """ReadModel의 적절한 위치를 계산합니다"""
        aggregate_id = action["ids"].get("aggregateId", "")
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
                "y": max_y + int(max_y_model["elementView"]["height"]/2) + int(read_model_object["elementView"]["height"]/2) + 14
            }
    
    @staticmethod
    def _get_query_parameters(es_value: Dict[str, Any], action: Dict[str, Any]) -> List[Dict[str, Any]]:
        """ReadModel의 쿼리 파라미터를 생성합니다"""
        if action["args"].get("queryParameters"):
            return [
                {
                    "className": prop.get("type", "String"),
                    "isCopy": False,
                    "isKey": prop.get("isKey", False),
                    "name": prop.get("name", ""),
                    "nameCamelCase": camel_case(prop.get("name", "")),
                    "namePascalCase": pascal_case(prop.get("name", "")),
                    "displayName": prop.get("displayName", ""),
                    "_type": "org.uengine.model.FieldDescriptor"
                }
                for prop in action["args"].get("queryParameters", [])
            ]
        
        aggregate = es_value["elements"].get(action["ids"].get("aggregateId", ""), {})
        if not aggregate or not aggregate.get("aggregateRoot") or not aggregate["aggregateRoot"].get("fieldDescriptors"):
            return []
            
        target_field_descriptors = aggregate["aggregateRoot"]["fieldDescriptors"]
        if action["args"].get("api_verb") == "DELETE":
            target_field_descriptors = [fd for fd in target_field_descriptors if fd.get("isKey")]
        
        return [
            {
                "className": prop.get("className", "String"),
                "isCopy": False,
                "isKey": prop.get("isKey", False),
                "name": prop.get("name", ""),
                "nameCamelCase": prop.get("nameCamelCase", ""),
                "namePascalCase": prop.get("namePascalCase", ""),
                "displayName": prop.get("displayName", ""),
                "_type": "org.uengine.model.FieldDescriptor"
            }
            for prop in target_field_descriptors
        ]