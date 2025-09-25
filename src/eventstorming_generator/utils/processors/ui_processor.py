from typing import Dict, Any, List

from ..convert_case_util import CaseConvertUtil
from ..es_utils import EsUtils

class UIProcessor:
    @staticmethod
    def get_action_applied_es_value(action: Dict[str, Any], user_info: Dict[str, Any], 
                                   information: Dict[str, Any], es_value: Dict[str, Any], 
                                   callbacks: Dict[str, List]) -> None:
        """액션에 따라 UI를 처리합니다"""
        if action.type == "create":
            UIProcessor._create_ui(action, user_info, information, es_value, callbacks)
        elif action.get("type") == "update":
            UIProcessor._update_ui(action, user_info, information, es_value, callbacks)
    
    @staticmethod
    def _create_ui(action: Dict[str, Any], user_info: Dict[str, Any], 
                   information: Dict[str, Any], es_value: Dict[str, Any], 
                   callbacks: Dict[str, List]) -> None:
        """UI 생성 액션을 처리합니다"""
        ui_name = action.args.get("uiName", "")
        ui_alias = action.args.get("uiAlias", "")
        bounded_context_id = action.ids.get("boundedContextId", "")
        aggregate_id = action.ids.get("aggregateId", "")
        command_id = action.ids.get("commandId")
        read_model_id = action.ids.get("readModelId")
        ui_id = action.ids.get("uiId", EsUtils.get_uuid())
        run_time_template_html = action.args.get("runTimeTemplateHtml", "")
        description = action.args.get("description", "")

        # UI 객체 생성
        ui_object = UIProcessor._get_ui_base(
            user_info, ui_name, ui_alias, bounded_context_id, 
            aggregate_id, command_id, read_model_id, 0, 0, ui_id, run_time_template_html,
            description
        )
        
        # 위치 설정 - Command 또는 ReadModel의 왼쪽에 배치
        valid_position = UIProcessor._get_valid_position(es_value, action, ui_object)
        ui_object["elementView"]["x"] = valid_position["x"]
        ui_object["elementView"]["y"] = valid_position["y"]

        # UI 객체 추가
        es_value["elements"][ui_object["id"]] = ui_object
    
    @staticmethod
    def _get_ui_base(user_info: Dict[str, Any], name: str, display_name: str,
                     bounded_context_id: str, aggregate_id: str, 
                     command_id: str = None, read_model_id: str = None,
                     x: int = 0, y: int = 0, element_uuid: str = None, 
                     run_time_template_html: str = "", description: str = "") -> Dict[str, Any]:
        """UI 기본 객체를 생성합니다"""
        element_uuid_to_use = element_uuid or EsUtils.get_uuid()

        return {
            "_type": "org.uengine.modeling.model.UI",
            "id": element_uuid_to_use,
            "name": name,
            "oldName": "",
            "displayName": display_name,
            "namePascalCase": CaseConvertUtil.pascal_case(name),
            "nameCamelCase": CaseConvertUtil.camel_case(name),
            "namePlural": CaseConvertUtil.plural(name),
            "description": description,
            "author": user_info.get("uid", ""),
            "boundedContext": {
                "id": bounded_context_id
            },
            "aggregate": {
                "id": aggregate_id
            },
            "command": {
                "id": command_id
            } if command_id else None,
            "readModel": {
                "id": read_model_id  
            } if read_model_id else None,
            "elementView": {
                "_type": "org.uengine.modeling.model.UI",
                "id": element_uuid_to_use,
                "x": x,
                "y": y,
                "width": 100,
                "height": 100,
                "style": {}
            },
            "uiType": "Chart",
            "chart": {
                "type": "",
                "fieldMapping": {
                    "category": [],
                    "data": []
                }
            },
            "grid": {
                "columns": []
            },
            "card": {
                "title": "",
                "subtitle": "",
                "text": ""
            },
            "runTimeTemplateHtml": run_time_template_html,
            "rotateStatus": False,
            "generateDescription": ""
        }
    
    @staticmethod
    def _get_valid_position(es_value: Dict[str, Any], action: Dict[str, Any], 
                           ui_object: Dict[str, Any]) -> Dict[str, int]:
        """UI의 적절한 위치를 계산합니다 (Command 또는 ReadModel의 왼쪽)"""
        command_id = action.ids.get("commandId")
        read_model_id = action.ids.get("readModelId")
        
        target_element = None
        if command_id:
            target_element = es_value["elements"].get(command_id)
        elif read_model_id:
            target_element = es_value["elements"].get(read_model_id)
        
        if not target_element:
            return {"x": 0, "y": 0}
        
        # 타겟 엘리먼트의 왼쪽에 UI를 배치
        target_view = target_element.get("elementView", {})
        ui_width = ui_object["elementView"]["width"]
        
        return {
            "x": target_view.get("x", 0) - int(target_view.get("width", 100)/2) - int(ui_width/2) + 19,
            "y": target_view.get("y", 0)
        }

    @staticmethod
    def make_ui_to_element(es_value: Dict[str, Any], action: Dict[str, Any], 
                            element_object: Dict[str, Any], user_info: Dict[str, Any]) -> None:
        """Element와 연결된 UI를 생성합니다"""          

        ui_name = element_object.get("name", "") + "UI"
        ui_alias = element_object.get("displayName", "") + " UI"
        bounded_context_id = action.ids.get("boundedContextId", "")
        aggregate_id = action.ids.get("aggregateId", "")
        command_id = action.ids.get("commandId")
        read_model_id = action.ids.get("readModelId")
        ui_id = action.ids.get("uiId", EsUtils.get_uuid())
        run_time_template_html = action.args.get("runTimeTemplateHtml", "")

        # UI 객체 생성
        ui_object = UIProcessor._get_ui_base(
            user_info, ui_name, ui_alias, bounded_context_id, 
            aggregate_id, command_id, read_model_id, 0, 0, ui_id, run_time_template_html
        )

        # 위치 설정 - Command 또는 ReadModel의 왼쪽에 배치
        valid_position = UIProcessor._get_valid_position(es_value, action, ui_object)
        ui_object["elementView"]["x"] = valid_position["x"]
        ui_object["elementView"]["y"] = valid_position["y"]

        # UI 객체 추가
        es_value["elements"][ui_object["id"]] = ui_object
        return ui_object

    @staticmethod
    def _update_ui(action: Dict[str, Any], user_info: Dict[str, Any], 
                     information: Dict[str, Any], es_value: Dict[str, Any], 
                     callbacks: Dict[str, List]) -> None:
        """기존 UI를 업데이트합니다"""
        ui_id = action.get("ids", {}).get("uiId", "")
        ui_object = es_value["elements"].get(ui_id)
        
        if not ui_object:
            return
        
        if action.args.get("runTimeTemplateHtml"):
            ui_object["runTimeTemplateHtml"] = action.args.get("runTimeTemplateHtml", "")

        if action.args.get("description"):
            ui_object["description"] = action.args.get("description", "")
        
        es_value["elements"][ui_id] = ui_object