import os

from ..test_utils import TestUtils
from ...generators import AssignCommandViewNamesToAggregateDraft
from ..mocks import assign_command_view_names_to_aggregate_draft_generator_inputs
from ...utils import LoggingUtil

def test_assign_command_view_names_to_aggregate_draft():
    try:

        result = AssignCommandViewNamesToAggregateDraft(os.getenv("AI_MODEL"), {}, {
            "preferredLanguage": "Korean",
            "inputs": {
                "aggregateDrafts": assign_command_view_names_to_aggregate_draft_generator_inputs["aggregateDrafts"],
                "siteMap": assign_command_view_names_to_aggregate_draft_generator_inputs["siteMap"]
            }
        }).generate()
        TestUtils.save_dict_to_temp_file(result, "test_assign_command_view_names_to_aggregate_draft")

    except Exception as e:
        LoggingUtil.exception("test_assign_command_view_names_to_aggregate_draft", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_assign_command_view_names_to_aggregate_draft_error")
        raise
