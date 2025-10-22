from .run_main_graph import run_main_graph
from .sub_graph.run_sub_graph import run_sub_graph
from .worker_subgraph.run_worker_sub_graph import run_worker_sub_graph

run_graph_registry = {
    "MainGraph": {
        "handler": run_main_graph,
        "description": "메인 그래프를 전체를 즉시 실행",
        "usage": "run runGraph MainGraph"
    },
    "SubGraph": {
        "handler": run_sub_graph,
        "description": "서브그래프를 즉시 실행",
        "usage": "run runGraph SubGraph <서브그래프 이름>"
    },
    "WorkerSubGraph": {
        "handler": run_worker_sub_graph,
        "description": "워커 서브그래프를 즉시 실행",
        "usage": "run runGraph WorkerSubGraph <워커 서브그래프 이름>"
    }
}

def run_graph(command_args):
    graph_name = command_args[0]

    graph = run_graph_registry.get(graph_name, None)
    if not graph:
        print(f"유효하지 않은 그래프 명령어입니다. {graph_name}")
        return False
    return graph["handler"](command_args)