from ..test_utils import TestUtils
from ...utils import LoggingUtil, XmlUtil
from ..mocks import xml_util_inputs

def test_xml_util():
    try:

        xml_string = XmlUtil.from_dict(xml_util_inputs, "root")
        LoggingUtil.info("test_xml_util", f"XML: {xml_string}")

    except Exception as e:
        LoggingUtil.exception("test_xml_util", f"테스트 실패", e)
        TestUtils.save_dict_to_temp_file({
            "error": str(e)
        }, "test_xml_util")
        raise