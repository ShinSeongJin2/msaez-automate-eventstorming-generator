import os

from ..test_utils import TestUtils
from ...generators import AssignDDLFieldsToAggregateDraft
from ..mocks import assign_ddl_fields_to_aggregate_draft_generator_inputs
from ...utils import LoggingUtil

def test_assign_ddl_fields_to_aggregate_draft():
    try:

        result = AssignDDLFieldsToAggregateDraft(os.getenv("AI_MODEL"), {}, {
            "preferredLanguage": "Korean",
            "inputs": {
                "description": assign_ddl_fields_to_aggregate_draft_generator_inputs["description"],
                "aggregateDrafts": assign_ddl_fields_to_aggregate_draft_generator_inputs["aggregateDrafts"],
                "allDdlFields": assign_ddl_fields_to_aggregate_draft_generator_inputs["allDdlFields"]
            }
        }).generate()
        TestUtils.save_dict_to_temp_file(result, "test_assign_ddl_fields_to_aggregate_draft")

    except Exception as e:
        LoggingUtil.exception("test_assign_ddl_fields_to_aggregate_draft", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_assign_ddl_fields_to_aggregate_draft_error")
        raise
