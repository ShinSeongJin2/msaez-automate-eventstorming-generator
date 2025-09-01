from typing import Dict, Any, List

from ..convert_case_util import CaseConvertUtil
from ..es_utils import EsUtils

class PolicyProcessor:
    @staticmethod
    def get_action_applied_es_value(action: Dict[str, Any], user_info: Dict[str, Any], 
                                   information: Dict[str, Any], es_value: Dict[str, Any], 
                                   callbacks: Dict[str, List]) -> None:
        """액션 유형에 따라 Policy를 처리합니다"""
        if action.get("type") == "create":
            PolicyProcessor._create_policy(action, user_info, information, es_value, callbacks)
    
    @staticmethod
    def _create_policy(action: Dict[str, Any], user_info: Dict[str, Any], 
                         information: Dict[str, Any], es_value: Dict[str, Any], 
                         callbacks: Dict[str, List]) -> None:
        """새로운 Policy를 생성합니다"""
        policy_name = action.get("args", {}).get("policyName", "")
        policy_alias = action.get("args", {}).get("policyAlias", "")
        reason = action.get("args", {}).get("reason", "")
        policy_id = action.get("ids", {}).get("policyId", "")
        refs = action.args.get("refs", [])
        source_bounded_context_id = action.args.get("sourceBoundedContextId", "")
        
        # boundedContextId, aggregateId는 outputEventIds를 통해 추론
        bounded_context_id = ""
        aggregate_id = ""
        output_event_ids = action.get("args", {}).get("outputEventIds", [])
        if output_event_ids:
            first_output_event_id = output_event_ids[0]
            # 이벤트는 이미 생성되어 있어야 함
            first_output_event = es_value["elements"].get(first_output_event_id)
            if first_output_event and first_output_event.get("aggregate"):
                bounded_context_id = first_output_event["boundedContext"]["id"]
                aggregate_id = first_output_event["aggregate"]["id"]

        # Policy 기본 객체 생성
        policy_object = PolicyProcessor._get_policy_base(
            user_info, policy_name, policy_alias, reason,
            bounded_context_id, aggregate_id, 0, 0, policy_id, refs, source_bounded_context_id
        )

        # 위치 설정
        valid_position = PolicyProcessor._get_valid_position(es_value, aggregate_id, policy_object)
        policy_object["elementView"]["x"] = valid_position["x"]
        policy_object["elementView"]["y"] = valid_position["y"]
        
        # Policy 객체 등록
        es_value["elements"][policy_object["id"]] = policy_object
        
        # 관계 생성을 위한 콜백 등록 (모든 객체가 생성된 후에 관계를 맺어야 함)
        PolicyProcessor._make_relations(policy_object, action, callbacks)
        
        # Aggregate 크기 조정
        EsUtils.resize_aggregate_vertically(es_value, policy_object)

    @staticmethod
    def _get_policy_base(user_info: Dict[str, Any], name: str, display_name: str, reason: str,
                        bounded_context_id: str, aggregate_id: str, 
                        x: int, y: int, element_uuid: str = None, 
                        refs: List[List[List[Any]]] = [],
                        source_bounded_context_id: str = "") -> Dict[str, Any]:
        """Policy 기본 객체를 생성합니다"""
        element_uuid_to_use = element_uuid or EsUtils.get_uuid()
        
        return {
            "id": element_uuid_to_use,
            "author": user_info.get("uid", ""),
            "boundedContext": {
                "id": bounded_context_id
            },
            "aggregate": {
                "id": aggregate_id
            },
            "description": reason,
            "elementView": {
                "height": 115,
                "width": 100,
                "x": x,
                "y": y,
                "id": element_uuid_to_use,
                "style": "{}",
                "_type": "org.uengine.modeling.model.Policy"
            },
            "fieldDescriptors": [],
            "hexagonalView": {
                "height": 20,
                "id": element_uuid_to_use,
                "style": "{}",
                "subWidth": 100,
                "width": 20,
                "_type": "org.uengine.modeling.model.PolicyHexagonal"
            },
            "isSaga": False,
            "name": name,
            "traceName": name,
            "displayName": display_name,
            "nameCamelCase": CaseConvertUtil.camel_case(name),
            "namePascalCase": CaseConvertUtil.pascal_case(name),
            "namePlural": CaseConvertUtil.plural(name),
            "oldName": "",
            "rotateStatus": False,
            "_type": "org.uengine.modeling.model.Policy",
            "refs": refs,
            "sourceBoundedContextId": source_bounded_context_id
        }
    
    @staticmethod
    def _make_relations(policy_object: Dict[str, Any], action: Dict[str, Any], callbacks: Dict[str, List]) -> None:
        """입력/출력 이벤트와 Policy 간의 관계를 생성합니다."""
        
        def create_relations_callback(es_value_cb: Dict[str, Any], user_info_cb: Dict[str, Any], information_cb: Dict[str, Any]):
            # Input Event -> Policy
            for event_id in action.get("args", {}).get("inputEventIds", []):
                event_object = es_value_cb["elements"].get(event_id)
                if event_object:
                    relation = EsUtils.getEventStormingRelationObjectBase(event_object, policy_object)
                    es_value_cb["relations"][relation["id"]] = relation

            # Policy -> Output Event
            for event_id in action.get("args", {}).get("outputEventIds", []):
                event_object = es_value_cb["elements"].get(event_id)
                if event_object:
                    relation = EsUtils.getEventStormingRelationObjectBase(policy_object, event_object)
                    es_value_cb["relations"][relation["id"]] = relation
        
        callbacks["afterAllObjectAppliedCallBacks"].append(create_relations_callback)

    @staticmethod
    def _get_valid_position(es_value: Dict[str, Any], aggregate_id: str, 
                           policy_object: Dict[str, Any]) -> Dict[str, int]:
        """Policy의 적절한 위치를 계산합니다"""
        return EsUtils.get_valid_position_for_left_side_element(es_value, aggregate_id, policy_object)