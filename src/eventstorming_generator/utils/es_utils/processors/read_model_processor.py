from typing import Dict, Any, List

from ...convert_case_util import CaseConvertUtil
from ..es_utils import EsUtils

class ReadModelProcessor:
    @staticmethod
    def get_action_applied_es_value(action: Dict[str, Any], user_id: str, project_id: str, 
                                   es_value: Dict[str, Any], callbacks: Dict[str, List]) -> None:
        """액션에 따라 ReadModel를 처리합니다"""
        if action["type"] == "create":
            ReadModelProcessor._create_read_model(action, user_id, project_id, es_value, callbacks)
    
    @staticmethod
    def _create_read_model(action: Dict[str, Any], user_id: str, project_id: str, es_value: Dict[str, Any], 
                         callbacks: Dict[str, List]) -> None:
        """ReadModel 생성 액션을 처리합니다"""
        read_model_name = action["args"].get("readModelName", "")
        read_model_alias = action["args"].get("readModelAlias", "")
        is_multiple_result = action["args"].get("isMultipleResult", False)
        bounded_context_id = action["ids"].get("boundedContextId", "")
        aggregate_id = action["ids"].get("aggregateId", "")
        read_model_id = action["ids"].get("readModelId", EsUtils.get_uuid())
        refs = action.args.get("refs", [])

        # ReadModel 객체 생성
        read_model_object = ReadModelProcessor._get_read_model_base(
            user_id, read_model_name, read_model_alias, is_multiple_result,
            bounded_context_id, aggregate_id, 0, 0, read_model_id, refs
        )
        
        # 위치 설정
        valid_position = ReadModelProcessor._get_valid_position(es_value, action, read_model_object)
        read_model_object["elementView"]["x"] = valid_position["x"]
        read_model_object["elementView"]["y"] = valid_position["y"]
        
        # Actor-UI-ReadModel 관계 설정
        def make_ui_and_actor_to_read_model(es_value: Dict[str, Any], user_id: str, project_id: str) -> None:
            from .ui_processor import UIProcessor
            from .actor_processor import ActorProcessor
            
            ui_object = UIProcessor.make_ui_to_element(es_value, action, read_model_object, user_id)
            ActorProcessor.make_actor_to_element(es_value, action, ui_object, user_id)
        callbacks["afterAllRelationAppliedCallBacks"].append(make_ui_and_actor_to_read_model)
        
        # 쿼리 파라미터 설정
        read_model_object["queryParameters"] = EsUtils.create_field_descriptors(action["args"].get("queryParameters", []))
        
        # ReadModel 객체 추가
        es_value["elements"][read_model_object["id"]] = read_model_object
        
        # Aggregate 크기 조정
        EsUtils.resize_aggregate_vertically(es_value, read_model_object)
    
    @staticmethod
    def _get_read_model_base(user_id: str, name: str, display_name: str, 
                           is_multiple_result: bool, bounded_context_id: str, 
                           aggregate_id: str, x: int, y: int, 
                           element_uuid: str = None, 
                           refs: List[List[List[Any]]] = []) -> Dict[str, Any]:
        """ReadModel 기본 객체를 생성합니다"""
        element_uuid_to_use = element_uuid or EsUtils.get_uuid()
        
        return {
            "_type": "org.uengine.modeling.model.View",
            "id": element_uuid_to_use,
            "visibility": "public",
            "name": name,
            "traceName": name,
            "oldName": "",
            "displayName": display_name,
            "namePascalCase": CaseConvertUtil.pascal_case(name),
            "namePlural": CaseConvertUtil.plural(name),
            "aggregate": {
                "id": aggregate_id
            },
            "description": None,
            "author": user_id,
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
            "definitionId": "",
            "refs": refs
        }
    
    @staticmethod
    def _get_valid_position(es_value: Dict[str, Any], action: Dict[str, Any], 
                          read_model_object: Dict[str, Any]) -> Dict[str, int]:
        """ReadModel의 적절한 위치를 계산합니다"""
        aggregate_id = action["ids"].get("aggregateId", "")
        return EsUtils.get_valid_position_for_left_side_element(es_value, aggregate_id, read_model_object)