import os

from ..test_utils import TestUtils
from ...generators import AssignEventNamesToAggregateDraft
from ..mocks import assign_event_names_to_aggregate_draft_generator_inputs
from ...utils import LoggingUtil

def test_assign_event_names_to_aggregate_draft():
    try:

        result = AssignEventNamesToAggregateDraft(os.getenv("AI_MODEL"), {}, {
            "preferredLanguage": "Korean",
            "inputs": {
                "boundedContextName": assign_event_names_to_aggregate_draft_generator_inputs["boundedContextName"],
                "aggregates": assign_event_names_to_aggregate_draft_generator_inputs["aggregates"],
                "eventNames": assign_event_names_to_aggregate_draft_generator_inputs["eventNames"]
            }
        }).generate()
        TestUtils.save_dict_to_temp_file(result, "test_assign_event_names_to_aggregate_draft")

    except Exception as e:
        LoggingUtil.exception("test_assign_event_names_to_aggregate_draft", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_assign_event_names_to_aggregate_draft_error")
        raise
