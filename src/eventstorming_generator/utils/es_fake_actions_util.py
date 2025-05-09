from typing import List
from ..models.action_model import ActionModel
from ..models.outputs import EsValueModel

class ESFakeActionsUtil:
    """
    AI 스트리밍시에 일부 액션이 반환된 상황에서도 이벤트 스토밍 구축시에 문제가 없도록
    가짜 액션을 추가하는 유틸리티 클래스
    """
    @staticmethod
    def add_fake_actions(actions: List[ActionModel], es_value: EsValueModel) -> List[ActionModel]:
        """
        액션 리스트에 필요한 가짜 액션들을 추가합니다.
        
        Args:
            actions: 처리할 액션 리스트
            es_value: 현재 이벤트 스토밍 값 객체
            
        Returns:
            가짜 액션이 추가된 액션 리스트
        """
        # BC, Aggregate인 경우에는 미리 생성되어 있어야 이벤트, 커맨드가 생성될 수 있기 때문에 해당 가짜 액션들을 앞단에 배치
        front_fake_actions = []
        back_fake_actions = []
        
        def getAllCreatedActions():
            return front_fake_actions + actions + back_fake_actions

        for action in actions:
            # 각 액션이 속한 엘리먼트의 id가 존재하지 않을 경우 발생하는 버그를 제거
            if action.ids:
                for id_key in action.ids:
                    # 자기 자신을 지칭하는 ID는 예외로 처리하기 위해서
                    if id_key.lower() in action.objectType.lower():
                        continue

                    id_to_check = action.ids[id_key]
                    if id_to_check in es_value.elements:
                        continue

                    if id_key == "boundedContextId":
                        if ESFakeActionsUtil._is_have_bc_create_action(getAllCreatedActions(), id_to_check):
                            continue
                        front_fake_actions.append(ESFakeActionsUtil._get_fake_bc_action(id_to_check))
                    
                    elif id_key == "aggregateId":
                        if ESFakeActionsUtil._is_have_aggregate_create_action(getAllCreatedActions(), id_to_check):
                            continue
                        front_fake_actions.append(ESFakeActionsUtil._get_fake_aggregate_action(action.ids["boundedContextId"], id_to_check))
                    # 나머지 타입들은 다른 객체가 속할 수 있는 엘리먼트가 아니기 때문에 확인할 필요가 없음

            # 커맨드가 호출시킬 이벤트가 없을 경우를 대비해서 가짜 이벤트 액션을 추가
            if action.objectType == "Command" and action.args and "outputEventIds" in action.args:
                for event_id in action.args["outputEventIds"]:
                    if event_id in es_value.elements:
                        continue
                    if ESFakeActionsUtil._is_have_event_create_action(getAllCreatedActions(), event_id):
                        continue
                    back_fake_actions.append(ESFakeActionsUtil._get_fake_event_action(
                        action.ids["boundedContextId"], action.ids["aggregateId"], event_id))

            # 이벤트가 정책으로 호출시킬 커맨드가 없는 경우를 대비해서 가짜 커맨드 액션을 추가
            if action.objectType == "Event" and action.args and "outputCommandIds" in action.args:
                for output_command in action.args["outputCommandIds"]:
                    command_id_to_check = output_command["commandId"]
                    if command_id_to_check in es_value.elements:
                        continue
                    if ESFakeActionsUtil._is_have_command_create_action(getAllCreatedActions(), command_id_to_check):
                        continue
                    back_fake_actions.append(ESFakeActionsUtil._get_fake_command_action(
                        action.ids["boundedContextId"], action.ids["aggregateId"], command_id_to_check))

        return getAllCreatedActions()

    @staticmethod
    def _is_have_bc_create_action(actions: List[ActionModel], id_to_check: str) -> bool:
        """주어진 ID의 BoundedContext 생성 액션이 있는지 확인"""
        return any(action.objectType == "BoundedContext" and action.ids.get("boundedContextId") == id_to_check for action in actions)

    @staticmethod
    def _is_have_aggregate_create_action(actions: List[ActionModel], id_to_check: str) -> bool:
        """주어진 ID의 Aggregate 생성 액션이 있는지 확인"""
        return any(action.objectType == "Aggregate" and action.ids.get("aggregateId") == id_to_check for action in actions)

    @staticmethod
    def _is_have_event_create_action(actions: List[ActionModel], id_to_check: str) -> bool:
        """주어진 ID의 Event 생성 액션이 있는지 확인"""
        return any(action.objectType == "Event" and action.ids.get("eventId") == id_to_check for action in actions)

    @staticmethod
    def _is_have_command_create_action(actions: List[ActionModel], id_to_check: str) -> bool:
        """주어진 ID의 Command 생성 액션이 있는지 확인"""
        return any(action.objectType == "Command" and action.ids.get("commandId") == id_to_check for action in actions)

    @staticmethod
    def _get_fake_bc_action(bounded_context_id: str) -> ActionModel:
        """가짜 BoundedContext 액션 생성"""
        return ActionModel(
            objectType="BoundedContext",
            ids={
                "boundedContextId": bounded_context_id
            },
            args={
                "boundedContextName": "BoundedContext " + bounded_context_id[:4]
            }
        )

    @staticmethod
    def _get_fake_aggregate_action(bounded_context_id: str, aggregate_id: str) -> ActionModel:
        """가짜 Aggregate 액션 생성"""
        return ActionModel(
            objectType="Aggregate",
            ids={
                "boundedContextId": bounded_context_id,
                "aggregateId": aggregate_id
            },
            args={
                "aggregateName": "Aggregate " + aggregate_id[:4],
                "properties": [
                    {
                        "name": "id",
                        "type": "Long",
                        "isKey": True
                    }
                ]
            }
        )

    @staticmethod
    def _get_fake_event_action(bounded_context_id: str, aggregate_id: str, event_id: str) -> ActionModel:
        """가짜 Event 액션 생성"""
        return ActionModel(
            objectType="Event",
            ids={
                "boundedContextId": bounded_context_id,
                "aggregateId": aggregate_id,
                "eventId": event_id
            },
            args={
                "eventName": "Event " + event_id[:4],
                "properties": [
                    {
                        "name": "id",
                        "type": "Long",
                        "isKey": True
                    }
                ],
                "outputCommandIds": []
            }
        )

    @staticmethod
    def _get_fake_command_action(bounded_context_id: str, aggregate_id: str, command_id: str) -> ActionModel:
        """가짜 Command 액션 생성"""
        return ActionModel(
            objectType="Command",
            ids={
                "boundedContextId": bounded_context_id,
                "aggregateId": aggregate_id,
                "commandId": command_id
            },
            args={
                "commandName": "Command " + command_id[:4],
                "api_verb": "POST",
                "properties": [
                    {
                        "name": "id",
                        "type": "Long",
                        "isKey": True
                    }
                ],
                "outputEventIds": [],
                "actor": "Actor " + command_id[:4]
            }
        )