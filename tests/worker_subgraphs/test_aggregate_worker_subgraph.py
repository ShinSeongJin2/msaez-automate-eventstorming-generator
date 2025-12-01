from eventstorming_generator.models import State, AggregateGenerationState
from eventstorming_generator.terminal.commons.graph import execute_aggregate_worker_subgraph

class TestAggregateWorkerSubgraph:
    """AggregateWorkerSubgraph 테스트"""
    def test_aggregate_worker_subgraph(self):
        """AggregateWorkerSubgraph가 올바르게 실행되는지 테스트"""
        output = execute_aggregate_worker_subgraph()
        state: State = output["state"]
        completed_aggregate: AggregateGenerationState = output["completed_aggregate"]


        # 에러 로그가 없는지 확인
        logs_to_check = state.outputs.logs

        error_logs = []
        for log in logs_to_check:
            if log.level == "error":
                error_logs.append(log)

        assert len(error_logs) == 0, "에러 로그가 있습니다"

        # 완료된 바운디드 컨텍스트가 있는지 확인
        assert len(completed_aggregate.created_actions) > 0, "완료된 액션이 없습니다"