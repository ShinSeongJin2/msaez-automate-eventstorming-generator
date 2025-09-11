from typing import List

from ...models import ActionModel, EsValueModel
from ...utils import EsActionsUtil, EsAliasTransManager
from ..mocks import information, user_info, actionsCollection, total_action_test
from ..test_utils import TestUtils
from ...utils import LoggingUtil
from .mock_actions_builder import MockActionBuilder

def test_es_value_creation_with_actions_collection():
    try:

        es_value = EsValueModel()
        alias_trans_manager = EsAliasTransManager(es_value)

        result = es_value
        for actions in actionsCollection:
            uuid_actions = alias_trans_manager.trans_to_uuid_in_actions(actions)
            result = EsActionsUtil.apply_actions(result, uuid_actions, user_info, information)
        

        target_ui_element = None
        for element in result["elements"].values():
            if element["name"] == "LoanBookUI":
                target_ui_element = element
                break
        
        if target_ui_element:
            result = EsActionsUtil.apply_actions(result, [
                ActionModel(
                    objectType="UI",
                    type="update",
                    ids={"uiId": target_ui_element["id"]},
                    args={"runTimeTemplateHtml": "Updated Template HTML"}
                )
            ], user_info, information)
        

        TestUtils.save_dict_to_temp_file(result, "test_es_value_creation_with_actions_collection")
        TestUtils.save_es_summarize_result_to_temp_file(result, "test_es_value_creation_with_actions_collection")

    except Exception as e:
        LoggingUtil.exception("test_es_value_creation_with_actions_collection", "테스트 실패", e)
        TestUtils.save_dict_to_temp_file(
            {
                "error": str(e),
                "user_info": user_info,
                "information": information,
            },
            "test_es_value_creation_with_actions_collection_error",
        )
        raise

def test_es_value_creation_total_action_test():
    try:

        result = EsActionsUtil.apply_actions(total_action_test["esValue"], total_action_test["actions"], user_info, information) 
        TestUtils.save_dict_to_temp_file(result, "test_es_value_creation_total_action_test")
        TestUtils.save_es_summarize_result_to_temp_file(result, "test_es_value_creation_total_action_test")

    except Exception as e:
        LoggingUtil.exception("test_es_value_creation_total_action_test", "테스트 실패", e)
        TestUtils.save_dict_to_temp_file(
            {
                "error": str(e),
                "user_info": user_info,
                "information": information,
            },
            "test_es_value_creation_total_action_test_error",
        )
        raise

def test_es_value_creation_with_mocked_actions():
    try:

        es_value = EsValueModel()
        alias_trans_manager = EsAliasTransManager(es_value)

        actionsCollection = [_make_mocked_actions([[6, 5, 7]] * 4)]

        result = es_value
        for actions in actionsCollection:
            uuid_actions = alias_trans_manager.trans_to_uuid_in_actions(actions)
            result = EsActionsUtil.apply_actions(result, uuid_actions, user_info, information)
        
        TestUtils.save_dict_to_temp_file(result, "test_es_value_creation_with_mocked_actions")
        TestUtils.save_es_summarize_result_to_temp_file(result, "test_es_value_creation_with_mocked_actions")

    except Exception as e:
        LoggingUtil.exception("test_es_value_creation_with_mocked_actions", "테스트 실패", e)
        TestUtils.save_dict_to_temp_file(
            {
                "error": str(e),
                "user_info": user_info,
                "information": information,
            },
            "test_es_value_creation_with_mocked_actions_error",
        )
        raise

def _make_mocked_actions(mock_info: List[List[int]]) -> List[ActionModel]:
    builder = MockActionBuilder()
    for bc_index, aggregates in enumerate(mock_info, 1):
        builder.with_bounded_context(bc_index)
        for agg_index, command_count in enumerate(aggregates, 1):
            builder.with_aggregate(agg_index)
            builder.with_command_event_pairs(command_count)
    return builder.build()