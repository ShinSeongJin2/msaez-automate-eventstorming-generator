from ..run_util import RunUtil
from ...utils import LoggingUtil, XmlUtil
from ..mocks import xml_util_inputs

def run_xml_util():
    run_name = "run_xml_util"

    try:

        xml_string = XmlUtil.from_dict(xml_util_inputs, "root")
        LoggingUtil.info(run_name, f"XML: {xml_string}")

    except Exception as e:
        LoggingUtil.exception(run_name, f"실행 실패", e)
        RunUtil.save_dict_to_temp_file({
            "error": str(e)
        }, f"{run_name}_error")
        raise