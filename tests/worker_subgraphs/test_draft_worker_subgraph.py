from eventstorming_generator.models import State, DraftGenerationState
from eventstorming_generator.terminal.commons.graph import execute_draft_worker_subgraph

class TestDraftWorkerSubgraph:
    """DraftWorkerSubgraph 테스트"""
    def test_draft_worker_subgraph(self):
        """DraftWorkerSubgraph가 올바르게 실행되는지 테스트"""
        output = execute_draft_worker_subgraph()
        state: State = output["state"]
        completed_draft: DraftGenerationState = output["completed_draft"]


        # 에러 로그가 없는지 확인
        logs_to_check = state.outputs.logs

        error_logs = []
        for log in logs_to_check:
            if log.level == "error":
                error_logs.append(log)

        assert len(error_logs) == 0, "에러 로그가 있습니다"

        # 완료된 Draft가 있는지 확인
        assert completed_draft.created_draft is not None and \
               len(completed_draft.created_draft.boundedContextName) > 0 and \
               len(completed_draft.created_draft.aggregates) > 0, "완료된 Draft가 없습니다"