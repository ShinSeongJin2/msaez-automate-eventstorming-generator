from eventstorming_generator.models import State, BoundedContextGenerationState
from eventstorming_generator.terminal.commons.graph import execute_bounded_context_worker_subgraph

class TestBoundedContextWorkerSubgraph:
    """BoundedContextWorkerSubgraph 테스트"""
    def test_bounded_context_worker_subgraph(self):
        """BoundedContextWorkerSubgraph가 올바르게 실행되는지 테스트"""
        output = execute_bounded_context_worker_subgraph()
        state: State = output["state"]
        completed_bounded_context: BoundedContextGenerationState = output["completed_bounded_context"]


        # 에러 로그가 없는지 확인
        logs_to_check = state.outputs.logs

        error_logs = []
        for log in logs_to_check:
            if log.level == "error":
                error_logs.append(log)

        assert len(error_logs) == 0, "에러 로그가 있습니다"

        # 완료된 바운디드 컨텍스트가 있는지 확인
        assert len(completed_bounded_context.created_bounded_contexts) > 0, "완료된 바운디드 컨텍스트가 없습니다"