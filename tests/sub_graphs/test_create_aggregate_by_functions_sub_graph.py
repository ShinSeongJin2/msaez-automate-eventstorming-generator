from eventstorming_generator.models import State
from eventstorming_generator.config import Config
from eventstorming_generator.systems import DatabaseFactory, MemoryDBSystem
from eventstorming_generator.terminal.commons.graph import execute_create_aggregate_by_functions_sub_graph
from eventstorming_generator.terminal.commons.mocks import create_aggregate_by_functions_sub_graph_inputs
from eventstorming_generator.terminal.terminal_tests.terminal_test_helper import TerminalTestHelper


class TestCreateAggregateByFunctionsSubGraph:
    """CreateAggregateByFunctionsSubGraph 테스트"""
    def test_create_aggregate_by_functions_sub_graph(self):
        """CreateAggregateByFunctionsSubGraph가 올바르게 실행되는지 테스트"""
        Config.set_db_type("memory")
        db_system: MemoryDBSystem = DatabaseFactory.get_db_system()
        db_system.clear()

        state: State = execute_create_aggregate_by_functions_sub_graph()
        TerminalTestHelper.test_state_by_after_stop_node(
            "create_aggregate_by_functions", create_aggregate_by_functions_sub_graph_inputs, state
        )