import time
import re
from typing import Callable
from langgraph.graph import StateGraph, START

from ..models import State, ElementNamesGenerationState, CreateElementNamesByDraftsOutput
from ..generators import CreateElementNamesByDrafts
from ..utils import JsonUtil, LogUtil, JobUtil
from ..constants import ResumeNodes
from ..config import Config


def resume_from_create_element_names(state: State):
    try :

        state.subgraphs.createElementNamesByDraftsModel.start_time = time.time()
        if state.outputs.lastCompletedRootGraphNode == ResumeNodes["ROOT_GRAPH"]["CREATE_ELEMENT_NAMES"] and state.outputs.lastCompletedSubGraphNode:
            if state.outputs.lastCompletedSubGraphNode in ResumeNodes["CREATE_ELEMENT_NAMES"].values():
                LogUtil.add_info_log(state, f"[CREATE_ELEMENT_NAMES_SUBGRAPH] Resuming from checkpoint: '{state.outputs.lastCompletedSubGraphNode}'")
                return state.outputs.lastCompletedSubGraphNode
            else:
                state.subgraphs.createElementNamesByDraftsModel.is_failed = True
                LogUtil.add_error_log(state, f"[CREATE_ELEMENT_NAMES_SUBGRAPH] Invalid checkpoint node: '{state.outputs.lastCompletedSubGraphNode}'")
                return "complete"
        
        LogUtil.add_info_log(state, "[CREATE_ELEMENT_NAMES_SUBGRAPH] Starting element names generation process")
        return "prepare"
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[CREATE_ELEMENT_NAMES_SUBGRAPH] Failed during resume_from_create_element_names", e)
        state.subgraphs.createElementNamesByDraftsModel.is_failed = True
        return "complete"

def prepare_element_names_generation(state: State) -> State:
    """
    각 BC별로 Element Names 생성을 위한 준비 작업 수행
    """
    
    try:

        LogUtil.add_info_log(state, "[CREATE_ELEMENT_NAMES_SUBGRAPH] Starting element names generation preparation")

        if state.subgraphs.createElementNamesByDraftsModel.is_processing:
            LogUtil.add_info_log(state, "[CREATE_ELEMENT_NAMES_SUBGRAPH] Element names generation already in progress, maintaining state")
            return state
        
        draft_options = state.inputs.selectedDraftOptions
        state.subgraphs.createElementNamesByDraftsModel.is_processing = True
        state.subgraphs.createElementNamesByDraftsModel.all_complete = False
        state.subgraphs.createElementNamesByDraftsModel.completed_generations = []
        
        pending_generations = []
        for bc_name, draft_option in draft_options.items():
            aggregateDraft = []
            for structure in draft_option.get("structure", []):
                aggregateDraft.append(structure.get("aggregate", {}))

            bounded_context = draft_option.get("boundedContext", {})
            bc_events = bounded_context.get("requirements", {}).get("event", [])

            event_names = []
            if bc_events:
                try:
                    event_names = re.findall(r'"name".*:.*"(.*?)"', bc_events)
                    event_names = [name for name in event_names if name]    
                except Exception as e:
                    LogUtil.add_error_log(state, f"[CREATE_ELEMENT_NAMES_SUBGRAPH] Failed to parse events for bounded context '{bc_name}': {e}")
                    event_names = []

            generation_state = ElementNamesGenerationState(
                previousElementNames={},
                target_bounded_context_name=bc_name,
                aggregate_draft=aggregateDraft,
                description=draft_option.get("description", ""),
                requested_event_names=event_names,
                requested_command_names=bounded_context.get("requirements", {}).get("commandNames", []),
                requested_read_model_names=bounded_context.get("requirements", {}).get("readModelNames", []),
                retry_count=0,
                generation_complete=False
            )
            pending_generations.append(generation_state)

        state.subgraphs.createElementNamesByDraftsModel.pending_generations = pending_generations
        
        LogUtil.add_info_log(state, f"[CREATE_ELEMENT_NAMES_SUBGRAPH] Preparation completed. Total bounded contexts to process: {len(pending_generations)}")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[CREATE_ELEMENT_NAMES_SUBGRAPH] Failed during element names generation preparation", e)
        state.subgraphs.createElementNamesByDraftsModel.is_failed = True
    
    return state

def select_next_element_names(state: State) -> State:
    """
    다음에 생성할 Element Names을 선택하고 현재 처리 상태로 설정
    """
    
    try:

        state.outputs.lastCompletedRootGraphNode = ResumeNodes["ROOT_GRAPH"]["CREATE_ELEMENT_NAMES"]
        state.outputs.lastCompletedSubGraphNode = ResumeNodes["CREATE_ELEMENT_NAMES"]["SELECT_NEXT"]
        JobUtil.update_job_to_firebase_fire_and_forget(state)

        if (not state.subgraphs.createElementNamesByDraftsModel.pending_generations and 
            not state.subgraphs.createElementNamesByDraftsModel.current_generation):
            state.subgraphs.createElementNamesByDraftsModel.all_complete = True
            state.subgraphs.createElementNamesByDraftsModel.is_processing = False
            return state
        
        if state.subgraphs.createElementNamesByDraftsModel.current_generation:
            return state
        
        if state.subgraphs.createElementNamesByDraftsModel.pending_generations:
            current_gen = state.subgraphs.createElementNamesByDraftsModel.pending_generations.pop(0)
            state.subgraphs.createElementNamesByDraftsModel.current_generation = current_gen
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[CREATE_ELEMENT_NAMES_SUBGRAPH] Failed to select next element names generation", e)
        state.subgraphs.createElementNamesByDraftsModel.is_failed = True
    
    return state

def preprocess_element_names_generation(state: State) -> State:
    """
    Element Names 생성을 위한 전처리 작업 수행
    """
    current_gen = state.subgraphs.createElementNamesByDraftsModel.current_generation
    if not current_gen:
        return state
        
    bc_name = current_gen.target_bounded_context_name
    
    try:

        current_gen.previousElementNames = state.subgraphs.createElementNamesByDraftsModel.extracted_element_names
        current_gen.is_preprocess_completed = True
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[CREATE_ELEMENT_NAMES_SUBGRAPH] Preprocessing failed for bounded context: '{bc_name}'", e)
        state.subgraphs.createElementNamesByDraftsModel.is_failed = True
    
    return state

def generate_element_names(state: State) -> State:
    """
    Element Names 생성 실행
    """
    current_gen = state.subgraphs.createElementNamesByDraftsModel.current_generation
    if not current_gen:
        LogUtil.add_info_log(state, "[CREATE_ELEMENT_NAMES_SUBGRAPH] No current element names generation to process")
        return state
        
    bc_name = current_gen.target_bounded_context_name
    
    try:

        generator = CreateElementNamesByDrafts(
            model_name=Config.get_ai_model(),
            client={
                "inputs": {
                    "previousElementNames": current_gen.previousElementNames,
                    "targetBoundedContextName": current_gen.target_bounded_context_name,
                    "aggregateDraft": current_gen.aggregate_draft,
                    "description": current_gen.description,
                    "requestedEventNames": current_gen.requested_event_names,
                    "requestedCommandNames": current_gen.requested_command_names,
                    "requestedReadModelNames": current_gen.requested_read_model_names,
                },
                "preferredLanguage": state.inputs.preferedLanguage
            }
        )
    
        generator_output:CreateElementNamesByDraftsOutput = generator.generate(current_gen.retry_count > 0, current_gen.retry_count)
        current_gen.extracted_element_names = generator_output.result.extracted_element_names
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[CREATE_ELEMENT_NAMES_SUBGRAPH] Failed to generate element names for bounded context: '{bc_name}'", e)
        if state.subgraphs.createElementNamesByDraftsModel.current_generation:
            state.subgraphs.createElementNamesByDraftsModel.current_generation.retry_count += 1
    
    return state

def postprocess_element_names_generation(state: State) -> State:
    """
    Element Names 생성 후처리 작업 수행
    """
    current_gen = state.subgraphs.createElementNamesByDraftsModel.current_generation
    if not current_gen:
        return state
        
    bc_name = current_gen.target_bounded_context_name
    try:
        if not current_gen.extracted_element_names:
            current_gen.retry_count += 1
            return state
        
        state.subgraphs.createElementNamesByDraftsModel.extracted_element_names[bc_name] = current_gen.extracted_element_names
        current_gen.generation_complete = True
        
        LogUtil.add_info_log(state, f"[CREATE_ELEMENT_NAMES_SUBGRAPH] Postprocessing completed successfully for bounded context: '{bc_name}'. Applied {len(current_gen.extracted_element_names)} element names to ES value")
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[CREATE_ELEMENT_NAMES_SUBGRAPH] Postprocessing failed for bounded context: '{bc_name}'", e)
        if current_gen:
            current_gen.retry_count += 1
            current_gen.extracted_element_names = {}
    
    return state

def validate_element_names_generation(state: State) -> State:
    """
    Element Names 생성 결과 검증 및 완료 처리
    """
    current_gen = state.subgraphs.createElementNamesByDraftsModel.current_generation
    if not current_gen:
        return state
        
    bc_name = current_gen.target_bounded_context_name
    try:

        if current_gen.generation_complete and not state.subgraphs.createElementNamesByDraftsModel.is_failed:
            # 변수 정리
            current_gen.previousElementNames = {}
            current_gen.target_bounded_context_name = ""
            current_gen.aggregate_draft = []
            current_gen.description = ""
            current_gen.requested_event_names = []
            current_gen.requested_command_names = []
            current_gen.requested_read_model_names = []
            current_gen.extracted_element_names = {}

            # 완료된 작업을 완료 목록에 추가
            state.subgraphs.createElementNamesByDraftsModel.completed_generations.append(current_gen)
            # 현재 작업 초기화
            state.subgraphs.createElementNamesByDraftsModel.current_generation = None
            state.outputs.currentProgressCount = state.outputs.currentProgressCount + 1
            
            total_progress = state.outputs.totalProgressCount
            current_progress = state.outputs.currentProgressCount
            LogUtil.add_info_log(state, f"[CREATE_ELEMENT_NAMES_SUBGRAPH] Element names generation completed successfully for bounded context: '{bc_name}'. Progress: {current_progress}/{total_progress}")

        elif current_gen.retry_count >= state.subgraphs.createElementNamesByDraftsModel.max_retry_count:
            state.subgraphs.createElementNamesByDraftsModel.is_failed = True
            LogUtil.add_error_log(state, f"[CREATE_ELEMENT_NAMES_SUBGRAPH] Element names generation failed after {current_gen.retry_count} retries for bounded context: '{bc_name}'.")
        else:
            LogUtil.add_info_log(state, f"[CREATE_ELEMENT_NAMES_SUBGRAPH] Retrying element names generation for bounded context: '{bc_name}' (attempt {current_gen.retry_count + 1}/{state.subgraphs.createElementNamesByDraftsModel.max_retry_count})")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[CREATE_ELEMENT_NAMES_SUBGRAPH] Validation failed for bounded context: '{bc_name}'", e)
        state.subgraphs.createElementNamesByDraftsModel.is_failed = True
    
    return state

def complete_processing(state: State) -> State:
    """
    Element Names 생성 프로세스 완료
    """
    try :

        state.outputs.lastCompletedRootGraphNode = ResumeNodes["ROOT_GRAPH"]["CREATE_ELEMENT_NAMES"]
        state.outputs.lastCompletedSubGraphNode = ResumeNodes["CREATE_ELEMENT_NAMES"]["COMPLETE"]
        JobUtil.update_job_to_firebase_fire_and_forget(state)

        completed_count = len(state.subgraphs.createElementNamesByDraftsModel.completed_generations)
        failed = state.subgraphs.createElementNamesByDraftsModel.is_failed
        
        if failed:
            LogUtil.add_error_log(state, f"[CREATE_ELEMENT_NAMES_SUBGRAPH] Element names generation process completed with failures. Successfully processed: {completed_count} bounded contexts")

        if not failed:
            # 변수 정리
            subgraph_model = state.subgraphs.createElementNamesByDraftsModel
            subgraph_model.current_generation = None
            subgraph_model.completed_generations = []
            subgraph_model.pending_generations = []
        
        state.subgraphs.createElementNamesByDraftsModel.end_time = time.time()
        state.subgraphs.createElementNamesByDraftsModel.total_seconds = state.subgraphs.createElementNamesByDraftsModel.end_time - state.subgraphs.createElementNamesByDraftsModel.start_time
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[CREATE_ELEMENT_NAMES_SUBGRAPH] Failed during element names generation process completion", e)
        state.subgraphs.createElementNamesByDraftsModel.is_failed = True

    return state

def decide_next_step(state: State) -> str:
    """
    다음 실행할 단계 결정
    """
    try :

        # 실패 시 완료 상태로 이동
        if state.subgraphs.createElementNamesByDraftsModel.is_failed:
            return "complete"

        # 모든 작업이 완료되었으면 완료 상태로 이동
        if state.subgraphs.createElementNamesByDraftsModel.all_complete:
            return "complete"
        
        # 현재 처리 중인 작업이 없으면 다음 작업 선택
        if not state.subgraphs.createElementNamesByDraftsModel.current_generation:
            return "select_next"
        
        current_gen = state.subgraphs.createElementNamesByDraftsModel.current_generation
        
        # 최대 재시도 횟수 초과 시 검증 단계로 이동 (실패 처리)
        if current_gen.retry_count >= state.subgraphs.createElementNamesByDraftsModel.max_retry_count:
            return "validate"
        
        # 현재 작업이 완료되었으면 검증 단계로 이동
        if current_gen.generation_complete:
            return "validate"
        
        # 전처리로 인한 요약 정보가 없을 경우, 전처리 단계로 이동
        if not current_gen.is_preprocess_completed:
            return "preprocess"
        
        # 기본적으로 생성 실행 단계로 이동
        if not current_gen.extracted_element_names:
            return "generate"
        
        # 생성된 Element Names이 있으면 후처리 단계로 이동
        return "postprocess"
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[CREATE_ELEMENT_NAMES_SUBGRAPH] Failed during decide_next_step", e)
        state.subgraphs.createElementNamesByDraftsModel.is_failed = True
        return "complete"

def create_element_names_by_draft_sub_graph() -> Callable:
    """
    Policy 액션 생성 서브그래프 생성
    """
    # 서브그래프 정의
    subgraph = StateGraph(State)
    
    # 노드 추가
    subgraph.add_node("prepare", prepare_element_names_generation)
    subgraph.add_node("select_next", select_next_element_names)
    subgraph.add_node("preprocess", preprocess_element_names_generation)
    subgraph.add_node("generate", generate_element_names)
    subgraph.add_node("postprocess", postprocess_element_names_generation)
    subgraph.add_node("validate", validate_element_names_generation)
    subgraph.add_node("complete", complete_processing)
    
    # 엣지 추가 (라우팅)
    subgraph.add_conditional_edges(START, resume_from_create_element_names, {
        "prepare": "prepare",
        "select_next": "select_next",
        "preprocess": "preprocess",
        "generate": "generate",
        "postprocess": "postprocess",
        "validate": "validate",
        "complete": "complete"
    })

    subgraph.add_conditional_edges(
        "prepare",
        decide_next_step,
        {
            "select_next": "select_next",
            "complete": "complete"
        }
    )
    
    subgraph.add_conditional_edges(
        "select_next",
        decide_next_step,
        {
            "select_next": "select_next",
            "preprocess": "preprocess",
            "complete": "complete"
        }
    )
    
    subgraph.add_conditional_edges(
        "preprocess",
        decide_next_step,
        {
            "generate": "generate",
            "complete": "complete"
        }
    )
    
    subgraph.add_conditional_edges(
        "generate",
        decide_next_step,
        {
            "postprocess": "postprocess",
            "generate": "generate",
            "validate": "validate",
            "complete": "complete"
        }
    )
    
    subgraph.add_conditional_edges(
        "postprocess",
        decide_next_step,
        {
            "validate": "validate",
            "generate": "generate",
            "complete": "complete"
        }
    )
    
    subgraph.add_conditional_edges(
        "validate",
        decide_next_step,
        {
            "select_next": "select_next",
            "preprocess": "preprocess",
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