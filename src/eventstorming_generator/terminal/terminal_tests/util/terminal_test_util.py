import os

terminal_test_util_registry = {
    "TextChunker": {
        "handler": lambda command_args: os.system("uv run pytest tests/utils/test_text_chunker.py -v"),
        "description": "TextChunker 테스트",
        "usage": "test testUtil TextChunker"
    },
    "JobRequestUtil": {
        "handler": lambda command_args: os.system("uv run pytest tests/utils/test_job_request_util.py -v"),
        "description": "JobRequestUtil 테스트",
        "usage": "test testUtil JobRequestUtil"
    },
    "XmlUtil": {
        "handler": lambda command_args: os.system("uv run pytest tests/utils/test_xml_util.py -v"),
        "description": "XmlUtil 테스트",
        "usage": "test testUtil XmlUtil"
    },
    "EsTraceUtil": {
        "handler": lambda command_args: os.system("uv run pytest tests/utils/test_es_trace_util.py -v"),
        "description": "EsTraceUtil 테스트",
        "usage": "test testUtil EsTraceUtil"
    }
}

def terminal_test_util(command_args):
    test_util_name = command_args[0]

    test_util = terminal_test_util_registry.get(test_util_name, None)
    if not test_util:
        print(f"유효하지 않은 유틸리티 명령어입니다. {test_util_name}")
        return False
    return test_util["handler"](command_args)