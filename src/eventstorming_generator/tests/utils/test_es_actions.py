from typing import List

from ...models import ActionModel, EsValueModel
from ...utils import EsActionsUtil, EsAliasTransManager
from ..mocks import information, user_info
from ..test_utils import TestUtils
from ...utils import LoggingUtil
from .mock_actions_builder import MockActionBuilder

def test_es_value_creation():
    try:

        es_value = EsValueModel()
        alias_trans_manager = EsAliasTransManager(es_value)

        mocked_actions = make_mocked_actions(
            [[2, 2], [2, 2], [2, 2], [2, 2], [2, 2]]
        ) # [[9, 5, 2], [2, 3], [6, 1], [4], [5, 3, 1, 5]]
        uuid_actions = alias_trans_manager.trans_to_uuid_in_actions(mocked_actions)
        result = EsActionsUtil.apply_actions(
            es_value, uuid_actions, user_info, information
        )

        TestUtils.save_dict_to_temp_file(result, "test_es_value_creation")
        TestUtils.save_es_summarize_result_to_temp_file(
            result, "test_es_value_creation"
        )

    except Exception as e:
        LoggingUtil.exception("test_es_value_creation", "테스트 실패", e)
        TestUtils.save_dict_to_temp_file(
            {
                "error": str(e),
                "user_info": user_info,
                "information": information,
            },
            "test_es_value_creation_error",
        )
        raise

def make_mocked_actions(mock_info: List[List[int]]) -> List[ActionModel]:
    builder = MockActionBuilder()
    for bc_index, aggregates in enumerate(mock_info, 1):
        builder.with_bounded_context(bc_index)
        for agg_index, command_count in enumerate(aggregates, 1):
            builder.with_aggregate(agg_index)
            builder.with_command_event_pairs(command_count)
    return builder.build()