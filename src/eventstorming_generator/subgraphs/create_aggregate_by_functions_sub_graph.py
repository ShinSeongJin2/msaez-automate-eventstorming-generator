import time
import uuid
from typing import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from langgraph.graph import StateGraph, START

from ..models import (
    AggregateGenerationState, State
)
from ..utils import JsonUtil, EsActionsUtil, JobUtil, LogUtil, CaseConvertUtil
from ..constants import ResumeNodes
from .worker_subgraphs import create_aggregate_worker_subgraph, aggregate_worker_id_context
from ..config import Config


def resume_from_create_aggregates(state: State):
    try :

        state.subgraphs.createAggregateByFunctionsModel.start_time = time.time()
        if state.outputs.lastCompletedRootGraphNode == ResumeNodes["ROOT_GRAPH"]["CREATE_AGGREGATES"] and state.outputs.lastCompletedSubGraphNode:
            if state.outputs.lastCompletedSubGraphNode in ResumeNodes["CREATE_AGGREGATES"].values():
                LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Resuming from checkpoint: '{state.outputs.lastCompletedSubGraphNode}'")
                return state.outputs.lastCompletedSubGraphNode
            else:
                state.subgraphs.createAggregateByFunctionsModel.is_failed = True
                LogUtil.add_error_log(state, f"[AGGREGATE_SUBGRAPH] Invalid checkpoint node: '{state.outputs.lastCompletedSubGraphNode}'")
                return "complete"
        
        LogUtil.add_info_log(state, "[AGGREGATE_SUBGRAPH] Starting aggregate generation process (parallel mode)")
        return "prepare"

    except Exception as e:
        LogUtil.add_exception_object_log(state, "[AGGREGATE_SUBGRAPH] Failed during resume_from_create_aggregates", e)
        state.subgraphs.createAggregateByFunctionsModel.is_failed = True
        return "complete"

def prepare_aggregate_generation(state: State) -> State:
    """
    초안으로부터 Aggregate 생성을 위한 준비 작업 수행
    - 초안 데이터 설정
    - DDL 필드 추출 및 애그리거트별 할당
    - 처리할 Aggregate 목록 초기화
    """
    
    try:
        # 이미 처리 중이면 상태 유지
        if state.subgraphs.createAggregateByFunctionsModel.is_processing:
            return state
        
        # 초안 데이터 설정
        state.subgraphs.createAggregateByFunctionsModel.is_processing = True
        state.subgraphs.createAggregateByFunctionsModel.all_complete = False
        
        # 처리할 Aggregate 목록 초기화
        pending_generations = []
        
        # 각 Bounded Context별로 처리할 Aggregate 추출
        for bounded_context_name, bounded_context_data in state.inputs.selectedDraftOptions.items():
            target_bounded_context = {"name": bounded_context_name}
            if "boundedContext" in bounded_context_data:
                target_bounded_context.update(bounded_context_data["boundedContext"])
            
            structures = bounded_context_data.get("structure", [])

            # 해당 Bounded Context의 구조 정보를 처리
            for structure in structures:
                description = bounded_context_data.get("description", {})
                # 각 Aggregate 구조에 대한 생성 상태 초기화
                generation_state = AggregateGenerationState(
                    target_bounded_context=target_bounded_context,
                    target_aggregate=structure.get("aggregate", {}),
                    description=description,
                    original_description=description,
                    draft_option=[{
                        "aggregate": structure.get("aggregate", {}),
                        "enumerations": structure.get("enumerations", []),
                        "valueObjects": structure.get("valueObjects", [])
                    }],
                    retry_count=0,
                    generation_complete=False,
                    requirements=target_bounded_context.get("requirements", {}),
                    ddl_fields=[CaseConvertUtil.camel_case(field) for field in structure.get("previewAttributes", [])]  # 할당된 DDL 필드 설정
                )
                pending_generations.append(generation_state)
        
        # 처리할 Aggregate 목록 저장
        state.subgraphs.createAggregateByFunctionsModel.pending_generations = pending_generations
        LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Preparation completed. Total aggregates to process: {len(pending_generations)}")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[AGGREGATE_SUBGRAPH] Failed during aggregate generation preparation", e)
        state.subgraphs.createAggregateByFunctionsModel.is_failed = True
    
    return state

def select_batch_aggregates(state: State) -> State:
    """
    다음 배치로 처리할 Aggregate들을 선택 (병렬 처리용)
    - batch_size만큼의 Aggregate를 한 번에 선택
    - current_batch에 설정하여 병렬 처리 준비
    """
    
    try:
        state.outputs.lastCompletedRootGraphNode = ResumeNodes["ROOT_GRAPH"]["CREATE_AGGREGATES"]
        state.outputs.lastCompletedSubGraphNode = ResumeNodes["CREATE_AGGREGATES"]["SELECT_BATCH"]
        JobUtil.update_job_to_firebase_fire_and_forget(state)

        model = state.subgraphs.createAggregateByFunctionsModel
        batch_size = Config.get_ai_model_light_max_batch_size()

        # 모든 처리가 완료되었는지 확인
        if not model.pending_generations and not model.current_batch:
            model.all_complete = True
            model.is_processing = False
            return state
        
        # 현재 처리 중인 배치가 있으면 상태 유지
        if model.current_batch:
            return state
        
        # 대기 중인 Aggregate들에서 배치 크기만큼 선택
        if model.pending_generations:
            # 남은 Aggregate 수와 배치 크기 중 작은 값만큼 선택
            actual_batch_size = min(batch_size, len(model.pending_generations))
            
            current_batch = []
            for _ in range(actual_batch_size):
                if model.pending_generations:
                    current_batch.append(model.pending_generations.pop(0))
            
            model.current_batch = current_batch
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[AGGREGATE_SUBGRAPH] Failed to select aggregate batch", e)
        state.subgraphs.createAggregateByFunctionsModel.is_failed = True
    
    return state

def execute_parallel_workers(state: State) -> State:
    """
    현재 배치의 Aggregate들을 병렬로 처리
    - 각 Aggregate를 개별 워커 서브그래프에서 병렬 실행
    - ThreadPoolExecutor를 사용하여 동시 처리
    """
    model = state.subgraphs.createAggregateByFunctionsModel
    
    if not model.current_batch:
        return state
    
    batch_size = len(model.current_batch)

    try:
        # 워커 서브그래프 인스턴스 생성
        worker_function = create_aggregate_worker_subgraph()
        
        # 각 Aggregate에 대해 워커 ID 생성 및 worker_generations에 저장
        worker_ids = []
        for aggregate_generation_state in model.current_batch:
            worker_id = str(uuid.uuid4())
            worker_ids.append(worker_id)
            model.worker_generations[worker_id] = aggregate_generation_state
        
        def execute_single_worker(worker_id: str) -> AggregateGenerationState:
            """
            단일 Aggregate를 워커에서 처리하는 함수 (메모리 최적화 버전)
            """
            try:
                # 현재 스레드의 컨텍스트에 worker_id 설정
                aggregate_worker_id_context.set(worker_id)

                aggregate_generation_state = model.worker_generations[worker_id]
                aggregate_name = aggregate_generation_state.target_aggregate.get("name", "Unknown")
                
                # 워커 실행
                result_state = worker_function(state)
                
                # 결과에서 처리된 Aggregate 상태 추출
                completed_aggregate = result_state.subgraphs.createAggregateByFunctionsModel.worker_generations.get(worker_id)
                
                if completed_aggregate and completed_aggregate.generation_complete:
                    return completed_aggregate
                elif completed_aggregate and completed_aggregate.is_failed:
                    LogUtil.add_error_log(state, f"[AGGREGATE_WORKER_EXECUTOR] Worker failed for aggregate '{aggregate_name}'")
                    return completed_aggregate
                else:
                    LogUtil.add_error_log(state, f"[AGGREGATE_WORKER_EXECUTOR] Worker returned incomplete result for aggregate '{aggregate_name}'")
                    aggregate_generation_state.is_failed = True
                    return aggregate_generation_state
                    
            except Exception as e:
                aggregate_generation_state = model.worker_generations.get(worker_id)
                if aggregate_generation_state:
                    aggregate_name = aggregate_generation_state.target_aggregate.get("name", "Unknown")
                    LogUtil.add_exception_object_log(state, f"[AGGREGATE_WORKER_EXECUTOR] Worker execution failed for aggregate '{aggregate_name}'", e)
                    aggregate_generation_state.is_failed = True
                    return aggregate_generation_state
                else:
                    LogUtil.add_exception_object_log(state, f"[AGGREGATE_WORKER_EXECUTOR] Worker execution failed for unknown worker_id: {worker_id}", e)
                    # 빈 실패 상태 반환
                    failed_state = AggregateGenerationState()
                    failed_state.is_failed = True
                    return failed_state
        
        # ThreadPoolExecutor를 사용한 병렬 실행
        with ThreadPoolExecutor(max_workers=batch_size) as executor:
            # 모든 워커 제출
            future_to_worker_id = {
                executor.submit(execute_single_worker, worker_id): worker_id 
                for worker_id in worker_ids
            }
            
            # 결과 수집
            completed_results = []
            for future in as_completed(future_to_worker_id):
                worker_id = future_to_worker_id[future]
                original_aggregate = model.worker_generations[worker_id]
                try:
                    result_aggregate = future.result()
                    completed_results.append(result_aggregate)
                    
                    aggregate_name = original_aggregate.target_aggregate.get("name", "Unknown")
                    
                except Exception as e:
                    aggregate_name = original_aggregate.target_aggregate.get("name", "Unknown")
                    LogUtil.add_exception_object_log(state, f"[AGGREGATE_SUBGRAPH] Failed to get worker result for aggregate '{aggregate_name}'", e)
                    original_aggregate.is_failed = True
                    completed_results.append(original_aggregate)
        
        # 결과를 parallel_worker_results에 저장
        model.parallel_worker_results = completed_results
        
        # 사용된 worker_generations 정리 (메모리 절약)
        for worker_id in worker_ids:
            if worker_id in model.worker_generations:
                del model.worker_generations[worker_id]
        
        successful_count = sum(1 for result in completed_results if result.generation_complete)
        failed_count = sum(1 for result in completed_results if result.is_failed)
        
        LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Parallel execution completed. Successful: {successful_count}, Failed: {failed_count}, Total: {len(completed_results)}")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[AGGREGATE_SUBGRAPH] Failed during parallel worker execution", e)
        model.is_failed = True
    
    return state

def collect_and_apply_results(state: State) -> State:
    """
    병렬 워커들의 결과를 수집하고 ES 모델에 적용
    - parallel_worker_results에서 결과 수집
    - 성공한 Aggregate들의 액션을 ES에 일괄 적용
    - 완료된 Aggregate들을 completed_generations로 이동
    """
    model = state.subgraphs.createAggregateByFunctionsModel
    
    if not model.parallel_worker_results:
        return state
    
    try:
        # 모든 성공한 Aggregate들의 액션 수집
        all_actions = []
        successful_aggregates = []
        failed_aggregates = []
        
        for aggregate_result in model.parallel_worker_results:
            aggregate_name = aggregate_result.target_aggregate.get("name", "Unknown")
            
            if aggregate_result.generation_complete and aggregate_result.created_actions:
                successful_aggregates.append(aggregate_result)
                all_actions.extend([action for action in aggregate_result.created_actions])
            else:
                failed_aggregates.append(aggregate_result)
                LogUtil.add_error_log(state, f"[AGGREGATE_SUBGRAPH] Aggregate '{aggregate_name}' failed or has no actions")
        
        # ES 모델에 모든 액션 일괄 적용
        if all_actions:   
            # 사용자 정보와 프로젝트 정보 준비
            user_info = state.inputs.userInfo or {}
            information = state.inputs.information or {}
            
            # EsActionsUtil을 사용하여 모든 액션 일괄 적용
            updated_es_value = EsActionsUtil.apply_actions(
                state.outputs.esValue.model_dump(),
                all_actions,
                user_info,
                information
            )
            
            # 업데이트된 ES 값 저장
            state.outputs.esValue = updated_es_value
            
        # 성공한 Aggregate들을 완료 목록으로 이동 (변수 정리)
        for aggregate in successful_aggregates:
            # 메모리 절약을 위한 변수 정리
            aggregate.target_bounded_context = {}
            aggregate.target_aggregate = {}
            aggregate.description = ""
            aggregate.original_description = ""
            aggregate.requirements = {}
            aggregate.draft_option = []
            aggregate.created_actions = []
            aggregate.extracted_ddl_fields = []
            aggregate.missing_ddl_fields = []
            aggregate.ddl_fields = []
            
            model.completed_generations.append(aggregate)
        
        # 실패한 Aggregate들도 완료 목록으로 이동 (재시도는 하지 않음)
        for aggregate in failed_aggregates:
            aggregate.target_bounded_context = {}
            aggregate.target_aggregate = {}
            aggregate.description = ""
            aggregate.original_description = ""
            aggregate.requirements = {}
            aggregate.draft_option = []
            aggregate.created_actions = []
            aggregate.extracted_ddl_fields = []
            aggregate.missing_ddl_fields = []
            aggregate.ddl_fields = []
            
            model.completed_generations.append(aggregate)
        
        # 배치 처리 완료 정리
        model.current_batch = []
        model.parallel_worker_results = []
        
        successful_count = len(successful_aggregates)
        failed_count = len(failed_aggregates)
        total_completed = len(model.completed_generations)
        
        LogUtil.add_info_log(state, f"[AGGREGATE_SUBGRAPH] Result collection completed. Batch - Successful: {successful_count}, Failed: {failed_count}. Total completed: {total_completed}")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[AGGREGATE_SUBGRAPH] Failed during result collection and application", e)
        model.is_failed = True
    
    return state

def complete_processing(state: State) -> State:
    """
    Aggregate 생성 프로세스 완료
    """
    
    try:

        state.outputs.lastCompletedRootGraphNode = ResumeNodes["ROOT_GRAPH"]["CREATE_AGGREGATES"]
        state.outputs.lastCompletedSubGraphNode = ResumeNodes["CREATE_AGGREGATES"]["COMPLETE"]
        state.outputs.currentProgressCount = state.outputs.currentProgressCount + 1
        JobUtil.update_job_to_firebase_fire_and_forget(state)

        completed_count = len(state.subgraphs.createAggregateByFunctionsModel.completed_generations)
        failed = state.subgraphs.createAggregateByFunctionsModel.is_failed
        
        if failed:
            LogUtil.add_error_log(state, f"[AGGREGATE_SUBGRAPH] Aggregate generation process completed with failures. Successfully processed: {completed_count} aggregates")

        if not failed:
            # 변수 정리
            subgraph_model = state.subgraphs.createAggregateByFunctionsModel
            subgraph_model.completed_generations = []
            subgraph_model.pending_generations = []
        
        state.subgraphs.createAggregateByFunctionsModel.end_time = time.time()
        state.subgraphs.createAggregateByFunctionsModel.total_seconds = state.subgraphs.createAggregateByFunctionsModel.end_time - state.subgraphs.createAggregateByFunctionsModel.start_time
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[AGGREGATE_SUBGRAPH] Failed during process completion", e)
        state.subgraphs.createAggregateByFunctionsModel.is_failed = True
    
    return state

def decide_next_step(state: State) -> str:
    """
    다음 실행할 단계 결정 (배치 처리 방식)
    """
    try:
        model = state.subgraphs.createAggregateByFunctionsModel

        if model.is_failed:
            return "complete"

        # 모든 작업이 완료되었으면 완료 상태로 이동
        if model.all_complete:
            return "complete"
        
        # 병렬 워커 결과가 있으면 결과 수집 및 적용 단계로 이동
        if model.parallel_worker_results:
            return "collect_results"
        
        # 현재 처리 중인 배치가 있으면 병렬 실행 단계로 이동
        if model.current_batch:
            return "execute_parallel"
        
        # 대기 중인 작업이 있으면 배치 선택 단계로 이동
        if model.pending_generations:
            return "select_batch"
            
        # 아무것도 없으면 완료
        return "complete"
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[AGGREGATE_SUBGRAPH] Failed during decide_next_step", e)
        state.subgraphs.createAggregateByFunctionsModel.is_failed = True
        return "complete"

def create_aggregate_by_functions_subgraph() -> Callable:
    """
    Aggregate 생성 서브그래프 생성
    """
    # 서브그래프 정의
    subgraph = StateGraph(State)
    
    # 새로운 배치 처리 노드들 추가
    subgraph.add_node("prepare", prepare_aggregate_generation)
    subgraph.add_node("select_batch", select_batch_aggregates)
    subgraph.add_node("execute_parallel", execute_parallel_workers)
    subgraph.add_node("collect_results", collect_and_apply_results)
    subgraph.add_node("complete", complete_processing)
    
    # 엣지 추가 (새로운 배치 처리 플로우)
    subgraph.add_conditional_edges(START, resume_from_create_aggregates, {
        "prepare": "prepare",
        "select_batch": "select_batch",
        "execute_parallel": "execute_parallel",
        "collect_results": "collect_results",
        "complete": "complete"
    })

    # 새로운 배치 처리 플로우 엣지들
    subgraph.add_conditional_edges(
        "prepare",
        decide_next_step,
        {
            "select_batch": "select_batch",
            "complete": "complete"
        }
    )
    
    subgraph.add_conditional_edges(
        "select_batch",
        decide_next_step,
        {
            "select_batch": "select_batch",
            "execute_parallel": "execute_parallel", 
            "complete": "complete"
        }
    )
    
    subgraph.add_conditional_edges(
        "execute_parallel",
        decide_next_step,
        {
            "collect_results": "collect_results",
            "complete": "complete"
        }
    )
    
    subgraph.add_conditional_edges(
        "collect_results",
        decide_next_step,
        {
            "select_batch": "select_batch",
            "complete": "complete"
        }
    )
    
    # 컴파일된 그래프 반환
    compiled_subgraph = subgraph.compile()
    
    # 서브그래프 실행 함수
    def run_subgraph(state: State) -> State:
        """
        서브그래프 실행 함수
        """
        # 서브그래프 실행
        result = State(**compiled_subgraph.invoke(state, {"recursion_limit": 2147483647}))
        return result
    
    return run_subgraph