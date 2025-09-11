from typing import List, Dict, Any
from ..models import EsValueModel, ActionModel
from .es_utils import EsUtils
from .processors import BoundedContextProcessor, AggregateProcessor, ValueObjectProcessor, EnumerationProcessor, CommandProcessor, EventProcessor, ReadModelProcessor, PolicyProcessor, UIProcessor
from .es_restore_actions_util import EsRestoreActionsUtil

class EsActionsUtil:
    @staticmethod
    def apply_actions(es_value: EsValueModel | Dict[str, Any], actions: List[ActionModel], 
                      user_info: Dict[str, Any], 
                      information: Dict[str, Any]) -> EsValueModel:
        """
        주어진 액션 목록을 적용하여 이벤트 스토밍 모델을 생성/업데이트합니다.
        
        Args:
            es_value: 기존 이벤트 스토밍 모델 (없으면 새로 생성)
            actions: 적용할 액션 목록
            user_info: 사용자 정보
            information: 프로젝트 정보
            
        Returns:
            업데이트된 이벤트 스토밍 모델
        """
        
        if hasattr(es_value, "model_dump"):
            es_dict = es_value.model_dump()
        else:
            es_dict = es_value
        
        EsRestoreActionsUtil.restoreActions(actions, es_dict)

        sorted_actions = EsActionsUtil._get_sorted_actions(actions)
        EsActionsUtil._ids_to_uuids(sorted_actions, es_dict)
        
        callbacks = {
            "afterAllObjectAppliedCallBacks": [],
            "afterAllRelationAppliedCallBacks": []
        }
        
        for action in sorted_actions:
            EsActionsUtil._apply_action(action, user_info, information, es_dict, callbacks)
        
        for callback in callbacks["afterAllObjectAppliedCallBacks"]:
            callback(es_dict, user_info, information)
            
        for callback in callbacks["afterAllRelationAppliedCallBacks"]:
            callback(es_dict, user_info, information)
            
        return EsValueModel(**es_dict)
    
    @staticmethod
    def _get_sorted_actions(actions: List[ActionModel]) -> List[ActionModel]:
        """액션을 처리 우선순위에 따라 정렬합니다"""
        priority_map = {
            'BoundedContext': 1,
            'Aggregate': 2,
            'GeneralClass': 3,
            'ValueObject': 4,
            'Enumeration': 5,
            'Event': 6,
            'Command': 7,
            'ReadModel': 8,
            'Policy': 9,
            'UI': 10
        }
        
        return sorted(actions, key=lambda a: priority_map.get(a.objectType, 999))
    
    @staticmethod
    def _ids_to_uuids(actions: List[ActionModel], es_value: Dict[str, Any]) -> None:
        """액션의 ID를 UUID로 변환합니다"""
        id_to_uuid_dic = {}
        
        for action in actions:
            for id_key in action.ids:
                action_id = action.ids[id_key]
                action.ids[id_key] = EsActionsUtil._get_or_create_uuid(action_id, id_to_uuid_dic, es_value)
      
            if "inputEventIds" in action.args:
                action.args["inputEventIds"] = [
                    EsActionsUtil._get_or_create_uuid(event_id, id_to_uuid_dic, es_value)
                    for event_id in action.args["inputEventIds"]
                ]
            
            if "outputEventIds" in action.args:
                action.args["outputEventIds"] = [
                    EsActionsUtil._get_or_create_uuid(event_id, id_to_uuid_dic, es_value)
                    for event_id in action.args["outputEventIds"]
                ]
    
    @staticmethod
    def _get_or_create_uuid(id_value: str, id_to_uuid_dic: Dict[str, str], es_value: Dict[str, Any]) -> str:
        """ID를 UUID로 변환하거나 이미 UUID인 경우 그대로 반환합니다"""
        import re
        
        uuid_regex = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.I)
        if uuid_regex.match(id_value):
            return id_value
        
        if id_value in es_value["elements"]:
            return id_value
        
        if id_value not in id_to_uuid_dic:
            id_to_uuid_dic[id_value] = EsUtils.get_uuid()
            
        return id_to_uuid_dic[id_value]
    
    @staticmethod
    def _apply_action(action: ActionModel, user_info: Dict[str, Any], 
                     information: Dict[str, Any], es_value: Dict[str, Any],
                     callbacks: Dict[str, List]) -> None:
        """액션 유형에 따라 적절한 처리 로직을 실행합니다"""
        if action.objectType == "BoundedContext":
            BoundedContextProcessor.get_action_applied_es_value(
                action, user_info, information, es_value, callbacks
            )
        elif action.objectType == "Aggregate":
            AggregateProcessor.get_action_applied_es_value(
                action, user_info, information, es_value, callbacks
            )
        elif action.objectType == "ValueObject":
            ValueObjectProcessor.get_action_applied_es_value(
                action, user_info, information, es_value, callbacks
            )
        elif action.objectType == "Enumeration":
            EnumerationProcessor.get_action_applied_es_value(
                action, user_info, information, es_value, callbacks
            )
        elif action.objectType == "Command":
            CommandProcessor.get_action_applied_es_value(
                action, user_info, information, es_value, callbacks
            )
        elif action.objectType == "Event":
            EventProcessor.get_action_applied_es_value(
                action, user_info, information, es_value, callbacks
            )
        elif action.objectType == "Policy":
            PolicyProcessor.get_action_applied_es_value(
                action, user_info, information, es_value, callbacks
            )
        elif action.objectType == "ReadModel":
            ReadModelProcessor.get_action_applied_es_value(
                action, user_info, information, es_value, callbacks
            )
        elif action.objectType == "UI":
            UIProcessor.get_action_applied_es_value(
                action, user_info, information, es_value, callbacks
            )