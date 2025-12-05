from .run_xml_util import run_xml_util
from .run_token_counter import run_token_counter
from .run_es_actions import run_es_actions
from .run_job_util import run_job_util
from .run_job_request_util import run_job_request_util
from .run_text_chunker_util import run_text_chunker_util
from .run_es_trace_util import run_es_trace_util

run_util_registry = {
    "XmlUtil": {
        "handler": run_xml_util,
        "description": "XmlUtil 유틸리티를 즉시 실행",
        "usage": "run runUtil XmlUtil"
    },
    "TokenCounter": {
        "handler": run_token_counter,
        "description": "TokenCounterUtil 유틸리티를 즉시 실행",
        "usage": "run runUtil TokenCounter"
    },
    "EsActions": {
        "handler": run_es_actions,
        "description": "EsActionsUtil 유틸리티를 즉시 실행",
        "usage": "run runUtil EsActions <actions_collection | total_actions | mocked_actions>"
    },
    "JobUtil": {
        "handler": run_job_util,
        "description": "JobUtil 유틸리티를 즉시 실행",
        "usage": "run runUtil JobUtil <createJobId>"
    },
    "JobRequestUtil": {
        "handler": run_job_request_util,
        "description": "JobRequestUtil 유틸리티를 즉시 실행",
        "usage": "run runUtil JobRequestUtil <addJobRequestByRequirements>"
    },
    "TextChunkerUtil": {
        "handler": run_text_chunker_util,
        "description": "TextChunkerUtil 유틸리티를 즉시 실행",
        "usage": "run runUtil TextChunkerUtil <splitIntoChunksByLine>"
    },
    "EsTraceUtil": {
        "handler": run_es_trace_util,
        "description": "EsTraceUtil 유틸리티를 즉시 실행",
        "usage": "run runUtil EsTraceUtil <convertRefsToIndexes>"
    }
}

def run_util(command_args):
    util_name = command_args[0]

    util = run_util_registry.get(util_name, None)
    if not util:
        print(f"유효하지 않은 유틸리티 명령어입니다. {util_name}")
        return False
    return util["handler"](command_args)