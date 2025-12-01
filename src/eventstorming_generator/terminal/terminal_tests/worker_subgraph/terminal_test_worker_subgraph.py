import os

terminal_test_worker_subgraph_registry = {
    "BoundedContextWorkerSubgraph": {
        "handler": lambda command_args: os.system("uv run pytest tests/worker_subgraphs/test_bounded_context_worker_subgraph.py -v"),
        "description": "BoundedContextWorkerSubgraph 테스트",
        "usage": "test testWorkerSubgraph BoundedContextWorkerSubgraph"
    },
    "ContextMappingWorkerSubgraph": {
        "handler": lambda command_args: os.system("uv run pytest tests/worker_subgraphs/test_context_mapping_worker_subgraph.py -v"),
        "description": "ContextMappingWorkerSubgraph 테스트",
        "usage": "test testWorkerSubgraph ContextMappingWorkerSubgraph"
    },
    "DraftWorkerSubgraph": {
        "handler": lambda command_args: os.system("uv run pytest tests/worker_subgraphs/test_draft_worker_subgraph.py -v"),
        "description": "DraftWorkerSubgraph 테스트",
        "usage": "test testWorkerSubgraph DraftWorkerSubgraph"
    },
    "AggregateWorkerSubgraph": {
        "handler": lambda command_args: os.system("uv run pytest tests/worker_subgraphs/test_aggregate_worker_subgraph.py -v"),
        "description": "AggregateWorkerSubgraph 테스트",
        "usage": "test testWorkerSubgraph AggregateWorkerSubgraph"
    }
}

def terminal_test_worker_subgraph(command_args):
    test_worker_subgraph_name = command_args[0]

    test_worker_subgraph = terminal_test_worker_subgraph_registry.get(test_worker_subgraph_name, None)
    if not test_worker_subgraph:
        print(f"유효하지 않은 워커 서브그래프 명령어입니다. {test_worker_subgraph_name}")
        return False
    return test_worker_subgraph["handler"](command_args)