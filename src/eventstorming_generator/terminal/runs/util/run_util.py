from .run_xml_util import run_xml_util
from .run_token_counter import run_token_counter
from .run_es_actions import run_es_actions

run_util_registry = {
    "XmlUtil": {
        "handler": run_xml_util,
        "description": "XML 유틸리티를 즉시 실행",
        "usage": "run runUtil XmlUtil"
    },
    "TokenCounter": {
        "handler": run_token_counter,
        "description": "토큰 수 계산",
        "usage": "run runUtil TokenCounter"
    },
    "EsActions": {
        "handler": run_es_actions,
        "description": "ES 액션 유틸리티를 실행시켜서, 이벤트 스토밍 값 생성",
        "usage": "run runUtil EsActions <actions_collection | total_actions | mocked_actions>"
    }
}

def run_util(command_args):
    util_name = command_args[0]

    util = run_util_registry.get(util_name, None)
    if not util:
        print(f"유효하지 않은 유틸리티 명령어입니다. {util_name}")
        return False
    return util["handler"](command_args)