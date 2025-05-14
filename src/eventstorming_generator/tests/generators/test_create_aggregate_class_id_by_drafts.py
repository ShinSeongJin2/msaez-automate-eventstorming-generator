from ..test_utils import TestUtils
from ...generators import CreateAggregateClassIdByDrafts
from ..mocks import create_aggregate_class_id_by_drafts_inputs
import os

def test_create_aggregate_class_id_by_drafts():
    try:

        result = CreateAggregateClassIdByDrafts(os.getenv("AI_MODEL"), {}, {
            "preferredLanguage": "Korean",
            "inputs": {
                "summarizedESValue": create_aggregate_class_id_by_drafts_inputs["summarizedESValue"],
                "draftOption": create_aggregate_class_id_by_drafts_inputs["draftOption"],
                "targetReferences": create_aggregate_class_id_by_drafts_inputs["targetReferences"]
            }
        }).generate()
        TestUtils.save_dict_to_temp_file(result, "test_create_aggregate_class_id_by_drafts")

    except Exception as e:
        print(f"테스트 실패: {str(e)}")
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_create_aggregate_class_id_by_drafts_error")
        raise
