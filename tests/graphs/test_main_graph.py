
from eventstorming_generator.config import Config
from eventstorming_generator.systems import DatabaseFactory, MemoryDBSystem
from eventstorming_generator.terminal.commons.graph import execute_main_graph_sequentially
from eventstorming_generator.terminal.terminal_tests.terminal_test_helper import TerminalTestHelper
from eventstorming_generator.models import State

class TestMainGraph:
    """MainGraph 테스트"""
    def test_main_graph_from_requirements(self):
        """MainGraph가 fromRequirements 요청 타입으로 올바르게 실행되는지 테스트"""
        Config.set_db_type("memory")
        db_system: MemoryDBSystem = DatabaseFactory.get_db_system()
        db_system.clear()
    
        def test_main_graph_callback(after_stop_node: str, previous_state: State, current_state: State):
            TerminalTestHelper.test_state_by_after_stop_node(after_stop_node, previous_state, current_state)
        
        execute_main_graph_sequentially(
            "fromRequirements", "library_requirements", "none", test_main_graph_callback
        )
    
    def test_main_graph_from_draft(self):
        """MainGraph가 fromDraft 요청 타입으로 올바르게 실행되는지 테스트"""
        Config.set_db_type("memory")
        db_system: MemoryDBSystem = DatabaseFactory.get_db_system()
        db_system.clear()
    
        def test_main_graph_callback(after_stop_node: str, previous_state: State, current_state: State):
            TerminalTestHelper.test_state_by_after_stop_node(after_stop_node, previous_state, current_state)
        
        execute_main_graph_sequentially(
            "fromDraft", "library_requirements", "none", test_main_graph_callback
        )