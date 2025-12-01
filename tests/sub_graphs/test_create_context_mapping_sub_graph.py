from eventstorming_generator.models import State
from eventstorming_generator.config import Config
from eventstorming_generator.systems import DatabaseFactory, MemoryDBSystem
from eventstorming_generator.terminal.commons.graph import execute_create_context_mapping_sub_graph
from eventstorming_generator.terminal.commons.mocks import create_context_mapping_sub_graph_inputs
from eventstorming_generator.terminal.terminal_tests.terminal_test_helper import TerminalTestHelper

class TestCreateContextMappingSubGraph:
    """CreateContextMappingSubGraph 테스트"""
    def test_create_context_mapping_sub_graph(self):
        """CreateContextMappingSubGraph가 올바르게 실행되는지 테스트"""
        Config.set_db_type("memory")
        db_system: MemoryDBSystem = DatabaseFactory.get_db_system()
        db_system.clear()

        state: State = execute_create_context_mapping_sub_graph()
        TerminalTestHelper.test_state_by_after_stop_node(
            "create_context_mapping", create_context_mapping_sub_graph_inputs, state
        )