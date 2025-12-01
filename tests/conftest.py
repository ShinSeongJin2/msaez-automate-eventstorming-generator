from dotenv import load_dotenv
from eventstorming_generator.config import Config

def pytest_configure(config):
    """pytest 설정 시 환경 변수 로드"""
    load_dotenv()
    Config.set_llm_cache_path('.cache/llm_cache_test.db')

def pytest_collection_modifyitems(items):
    """테스트 실행 순서를 커스터마이징"""
    priority_order = [
        'tests\\utils\\',
        'tests\\generators\\',
        'tests\\generator_utils\\',
        'tests\\sub_graph_utils\\',
        'tests\\worker_subgraphs\\',
        'tests\\sub_graphs\\',
        'tests\\graphs\\'
    ]
    
    def get_priority(item):
        item_path = str(item.fspath)
        for idx, pattern in enumerate(priority_order):
            if pattern in item_path:
                return idx
        return len(priority_order)
    
    items.sort(key=get_priority)