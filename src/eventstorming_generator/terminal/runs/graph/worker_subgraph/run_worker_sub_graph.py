from .run_bounded_context_worker_subgraph import run_bounded_context_worker_subgraph
from .run_context_mapping_worker_subgraph import run_context_mapping_worker_subgraph
from .run_draft_worker_subgraph import run_draft_worker_subgraph
from .run_aggregate_worker_subgraph import run_aggregate_worker_subgraph
from .run_class_id_worker_subgraph import run_class_id_worker_subgraph
from .run_command_actions_worker_subgraph import run_command_actions_worker_subgraph
from .run_gwt_worker_sub_graph import run_gwt_worker_sub_graph
from .run_policy_actions_worker_subgraph import run_policy_actions_worker_subgraph
from .run_ui_component_worker_subgraph import run_ui_component_worker_subgraph

run_worker_sub_graph_registry = {
    "BoundedContextWorkerSubGraph": {
        "handler": run_bounded_context_worker_subgraph,
        "description": "BoundedContextWorkerSubGraph를 즉시 실행",
        "usage": "run runGraph WorkerSubGraph BoundedContextWorkerSubGraph"
    },
    "ContextMappingWorkerSubGraph": {
        "handler": run_context_mapping_worker_subgraph,
        "description": "ContextMappingWorkerSubGraph를 즉시 실행",
        "usage": "run runGraph WorkerSubGraph ContextMappingWorkerSubGraph"
    },
    "DraftWorkerSubGraph": {
        "handler": run_draft_worker_subgraph,
        "description": "DraftWorkerSubGraph를 즉시 실행",
        "usage": "run runGraph WorkerSubGraph DraftWorkerSubGraph"
    },
    "AggregateWorkerSubGraph": {
        "handler": run_aggregate_worker_subgraph,
        "description": "AggregateWorkerSubGraph를 즉시 실행",
        "usage": "run runGraph WorkerSubGraph AggregateWorkerSubGraph"
    },
    "ClassIdWorkerSubGraph": {
        "handler": run_class_id_worker_subgraph,
        "description": "ClassIdWorkerSubGraph를 즉시 실행",
        "usage": "run runGraph WorkerSubGraph ClassIdWorkerSubGraph"
    },
    "CommandActionsWorkerSubGraph": {
        "handler": run_command_actions_worker_subgraph,
        "description": "CommandActionsWorkerSubGraph를 즉시 실행",
        "usage": "run runGraph WorkerSubGraph CommandActionsWorkerSubGraph"
    },
    "GwtWorkerSubGraph": {
        "handler": run_gwt_worker_sub_graph,
        "description": "GwtWorkerSubGraph를 즉시 실행",
        "usage": "run runGraph WorkerSubGraph GwtWorkerSubGraph"
    },
    "PolicyActionsWorkerSubGraph": {
        "handler": run_policy_actions_worker_subgraph,
        "description": "PolicyActionsWorkerSubGraph를 즉시 실행",
        "usage": "run runGraph WorkerSubGraph PolicyActionsWorkerSubGraph"
    },
    "UiComponentWorkerSubGraph": {
        "handler": run_ui_component_worker_subgraph,
        "description": "UiComponentWorkerSubGraph를 즉시 실행",
        "usage": "run runGraph WorkerSubGraph UiComponentWorkerSubGraph"
    }
}

def run_worker_sub_graph(command_args):
    worker_sub_graph_name = command_args[1]

    worker_sub_graph = run_worker_sub_graph_registry.get(worker_sub_graph_name, None)
    if not worker_sub_graph:
        print(f"유효하지 않은 워커 서브그래프 명령어입니다. {worker_sub_graph_name}")
        return False
    return worker_sub_graph["handler"](command_args)