import os
from typing import Callable, Dict, Any, List
from copy import deepcopy
from langgraph.graph import StateGraph, START

from ..models import CreateUiComponentsGenerationState, ActionModel, State
from ..utils import LogUtil, JobUtil, EsActionsUtil
from ..generators import CreateCommandWireFrame, CreateReadModelWireFrame
from ..constants import ResumeNodes


def resume_from_create_ui_components(state: State):
    try :

        if state.outputs.lastCompletedRootGraphNode == ResumeNodes["ROOT_GRAPH"]["CREATE_UI_COMPONENTS"] and state.outputs.lastCompletedSubGraphNode:
            if state.outputs.lastCompletedSubGraphNode in ResumeNodes["CREATE_UI_COMPONENTS"].values():
                LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Resuming from checkpoint: '{state.outputs.lastCompletedSubGraphNode}'")
                return state.outputs.lastCompletedSubGraphNode
            else:
                state.subgraphs.createUiComponentsModel.is_failed = True
                LogUtil.add_error_log(state, f"[UI_COMPONENTS_SUBGRAPH] Invalid checkpoint node: '{state.outputs.lastCompletedSubGraphNode}'")
                return "complete"
        
        LogUtil.add_info_log(state, "[UI_COMPONENTS_SUBGRAPH] Starting UI Components generation process")
        return "prepare"
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[UI_COMPONENTS_SUBGRAPH] Failed during resume_from_create_ui_components", e)
        state.subgraphs.createUiComponentsModel.is_failed = True
        return "complete"

def prepare_ui_components_generation(state: State) -> State:
    """
    UI 컴포넌트 생성을 위한 준비 작업 수행
    - UI 컴포넌트 탐색
    - 처리할 UI 컴포넌트 목록 초기화
    """
    
    try:
        LogUtil.add_info_log(state, "[UI_COMPONENTS_SUBGRAPH] Starting UI Components generation preparation")

        # 이미 처리 중이면 상태 유지
        if state.subgraphs.createUiComponentsModel.is_processing:
            LogUtil.add_info_log(state, "[UI_COMPONENTS_SUBGRAPH] UI Components generation already in progress, maintaining state")
            return state
        
        # 상태 초기화
        state.subgraphs.createUiComponentsModel.is_processing = True
        state.subgraphs.createUiComponentsModel.all_complete = False

        # 처리할 UI 컴포넌트 목록 초기화
        pending_generations = []
        total_ui_components = 0
        
        # ES 값에서 UI 컴포넌트 탐색
        es_value = state.outputs.esValue.model_dump()
        for element in es_value.get("elements", {}).values():
            if element and element.get("_type") == "org.uengine.modeling.model.UI":
                ui_name = element.get("name", "Unknown")
                LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Found UI Component: '{ui_name}'")
                
                # CreateUiComponentsGenerationState 생성
                generation_state = CreateUiComponentsGenerationState(
                    target_ui_component=deepcopy(element),
                    ai_request_type="",
                    ai_input_data={},
                    ui_replace_actions=[],
                    retry_count=0,
                    generation_complete=False,
                    is_failed=False
                )
                
                pending_generations.append(generation_state)
                total_ui_components += 1
                LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Queued UI generation for component '{ui_name}'")

        # 처리할 UI 생성 목록 저장
        state.subgraphs.createUiComponentsModel.pending_generations = pending_generations
        
        LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Preparation completed. Total UI components to process: {total_ui_components}")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[UI_COMPONENTS_SUBGRAPH] Failed during UI Components generation preparation", e)
        state.subgraphs.createUiComponentsModel.is_failed = True

    return state

def select_next_ui_components_generation(state: State) -> State:
    """
    다음에 생성할 UI 컴포넌트를 선택하고 현재 처리 상태로 설정
    """
    
    try:
        state.outputs.lastCompletedRootGraphNode = ResumeNodes["ROOT_GRAPH"]["CREATE_UI_COMPONENTS"]
        state.outputs.lastCompletedSubGraphNode = ResumeNodes["CREATE_UI_COMPONENTS"]["SELECT_NEXT"]
        JobUtil.update_job_to_firebase_fire_and_forget(state)

        pending_count = len(state.subgraphs.createUiComponentsModel.pending_generations)
        completed_count = len(state.subgraphs.createUiComponentsModel.completed_generations)
        
        LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Selecting next UI generation task. Pending: {pending_count}, Completed: {completed_count}")

        # 모든 처리가 완료되었는지 확인
        if (not state.subgraphs.createUiComponentsModel.pending_generations and 
            not state.subgraphs.createUiComponentsModel.current_generation):
            state.subgraphs.createUiComponentsModel.all_complete = True
            state.subgraphs.createUiComponentsModel.is_processing = False
            LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] All UI generation tasks completed successfully. Total processed: {completed_count} UI components")
            return state
        
        # 현재 처리 중인 작업이 있으면 상태 유지
        if state.subgraphs.createUiComponentsModel.current_generation:
            current = state.subgraphs.createUiComponentsModel.current_generation
            ui_name = current.target_ui_component.get("name", "Unknown")
            LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Current UI generation in progress for component '{ui_name}'")
            return state
        
        # 대기 중인 UI 생성이 있으면 첫 번째 항목을 현재 처리 상태로 설정
        if state.subgraphs.createUiComponentsModel.pending_generations:
            next_generation = state.subgraphs.createUiComponentsModel.pending_generations.pop(0)
            state.subgraphs.createUiComponentsModel.current_generation = next_generation
            
            ui_name = next_generation.target_ui_component.get("name", "Unknown")
            remaining_count = len(state.subgraphs.createUiComponentsModel.pending_generations)
            LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Selected next UI generation task for component '{ui_name}' (remaining: {remaining_count})")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[UI_COMPONENTS_SUBGRAPH] Failed to select next UI generation task", e)
        state.subgraphs.createUiComponentsModel.is_failed = True
    
    return state

def preprocess_ui_components_generation(state: State) -> State:
    """
    UI 컴포넌트 생성을 위한 전처리 작업 수행
    - UI 컴포넌트 타입 분석 (Command 또는 ReadModel)
    - AI 생성기에 필요한 입력 데이터 구성
    """
    current_gen = state.subgraphs.createUiComponentsModel.current_generation
    if not current_gen:
        LogUtil.add_info_log(state, "[UI_COMPONENTS_SUBGRAPH] No UI generation task currently being processed, skipping preprocessing")
        return state
        
    ui_name = current_gen.target_ui_component.get("name", "Unknown")
    LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Starting preprocessing for UI component '{ui_name}'")
    
    try:
        # siteMap ID 기반 접근을 위한 딕셔너리 구성
        site_map_id_info_dict = {}
        for bc_name, draft_option in state.inputs.selectedDraftOptions.items():
            siteMap = draft_option.get("boundedContext", {}).get("requirements", {}).get("siteMap", None)
            if not siteMap: 
                continue
            for site_map_object in siteMap:
                site_map_id_info_dict[site_map_object.get("id")] = site_map_object

        es_value = state.outputs.esValue.model_dump()
        target_ui_component = current_gen.target_ui_component
        
        # Command 연결 확인 및 처리
        if target_ui_component.get("command"):
            command_id = target_ui_component.get("command").get("id")
            command_element = es_value.get("elements", {}).get(command_id)
            
            if command_element:
                LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Processing Command type UI for '{ui_name}' (Command: {command_element.get('name')})")
                
                # Command 필드 정보 추출
                fields = []
                for field in command_element.get("fieldDescriptors", []):
                    fields.append({
                        "name": field.get("name"),
                        "type": field.get("className") or "String",
                        "required": field.get("isKey") or False
                    })
                
                # API 정보 구성
                api_method = command_element.get("controllerInfo", {}).get("method") or "POST"
                api_path = command_element.get("controllerInfo", {}).get("apiPath") or "N/A"
                api = f"{api_method} {api_path}"
                
                # 추가 요구사항 구성 (SiteMap 기반)
                referenced_site_map_id = command_element.get("referencedSiteMapId")
                additional_requirements = ""
                if referenced_site_map_id and referenced_site_map_id in site_map_id_info_dict:
                    site_map_object = site_map_id_info_dict[referenced_site_map_id]
                    additional_requirements = f"""This UI is included as part of the given sitemap. Please create the UI with these points in mind.
* SiteMap Info
- Bounded Context: {site_map_object.get("boundedContext", {})}
- Title: {site_map_object.get("title")}
- Description: {site_map_object.get("description")}
"""
                
                # AI 입력 데이터 구성
                current_gen.ai_request_type = "Command"
                current_gen.ai_input_data = {
                    "commandName": command_element.get("name"),
                    "commandDisplayName": command_element.get("displayName"),
                    "fields": fields,
                    "api": api,
                    "additionalRequirements": additional_requirements
                }
                
        # ReadModel 연결 확인 및 처리
        elif target_ui_component.get("readModel"):
            read_model_id = target_ui_component.get("readModel").get("id")
            read_model_element = es_value.get("elements", {}).get(read_model_id)
            
            if read_model_element:
                LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Processing ReadModel type UI for '{ui_name}' (ReadModel: {read_model_element.get('name')})")
                
                # ReadModel 쿼리 파라미터 추출
                view_query_parameters = []
                for query_param in read_model_element.get("queryParameters", []):
                    view_query_parameters.append({
                        "name": query_param.get("name"),
                        "type": query_param.get("className") or "String"
                    })
                
                # Aggregate 필드 정보 추출
                aggregate_id = read_model_element.get("aggregate", {}).get("id")
                aggregate_element = es_value.get("elements", {}).get(aggregate_id)
                aggregate_fields = []
                if aggregate_element:
                    aggregate_root = aggregate_element.get("aggregateRoot", {})
                    if aggregate_root:
                        for field in aggregate_root.get("fieldDescriptors", []):
                            aggregate_fields.append({
                                "name": field.get("name"),
                                "type": field.get("className") or "String"
                            })
                
                # 추가 요구사항 구성 (SiteMap 기반)
                referenced_site_map_id = read_model_element.get("referencedSiteMapId")
                additional_requirements = ""
                if referenced_site_map_id and referenced_site_map_id in site_map_id_info_dict:
                    site_map_object = site_map_id_info_dict[referenced_site_map_id]
                    additional_requirements = f"""This UI is included as part of the given sitemap. Please create the UI with these points in mind.
* SiteMap Info
- Bounded Context: {site_map_object.get("boundedContext", {})}
- Title: {site_map_object.get("title")}
- Description: {site_map_object.get("description")}
"""
                
                # AI 입력 데이터 구성
                current_gen.ai_request_type = "ReadModel"
                current_gen.ai_input_data = {
                    "viewName": read_model_element.get("name"),
                    "viewDisplayName": read_model_element.get("displayName"),
                    "aggregateFields": aggregate_fields,
                    "viewQueryParameters": view_query_parameters,
                    "additionalRequirements": additional_requirements
                }
        
        else:
            # Command도 ReadModel도 연결되지 않은 경우
            LogUtil.add_error_log(state, f"[UI_COMPONENTS_SUBGRAPH] UI component '{ui_name}' has no Command or ReadModel attached")
            current_gen.is_failed = True
            return state
        
        LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Preprocessing completed for UI component '{ui_name}' (Type: {current_gen.ai_request_type})")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[UI_COMPONENTS_SUBGRAPH] Preprocessing failed for UI component '{ui_name}'", e)
        current_gen.is_failed = True
    
    return state

def generate_ui_components_generation(state: State) -> State:
    """
    UI 컴포넌트 Wireframe 생성 실행
    - 적절한 Wireframe 생성기 호출
    - 결과를 ActionModel로 변환
    """
    current_gen = state.subgraphs.createUiComponentsModel.current_generation
    if not current_gen:
        LogUtil.add_info_log(state, "[UI_COMPONENTS_SUBGRAPH] No UI generation task currently being processed, skipping generation")
        return state
        
    ui_name = current_gen.target_ui_component.get("name", "Unknown")
    retry_info = f" (retry {current_gen.retry_count})" if current_gen.retry_count > 0 else ""
    LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Generating Wireframe for UI component '{ui_name}' (Type: {current_gen.ai_request_type}){retry_info}")
    
    try:
        # 모델명 가져오기
        model_name = os.getenv("AI_MODEL") or f"{state.inputs.llmModel.model_vendor}:{state.inputs.llmModel.model_name}"
        
        # AI 요청 타입에 따라 적절한 생성기 선택
        generator = None
        if current_gen.ai_request_type == "Command":
            generator = CreateCommandWireFrame(
                model_name=model_name,
                client={
                    "inputs": current_gen.ai_input_data,
                    "preferredLanguage": state.inputs.preferedLanguage
                }
            )
        elif current_gen.ai_request_type == "ReadModel":
            generator = CreateReadModelWireFrame(
                model_name=model_name,
                client={
                    "inputs": current_gen.ai_input_data,
                    "preferredLanguage": state.inputs.preferedLanguage
                }
            )
        else:
            LogUtil.add_error_log(state, f"[UI_COMPONENTS_SUBGRAPH] Invalid AI request type '{current_gen.ai_request_type}' for UI component '{ui_name}'")
            current_gen.is_failed = True
            return state
        
        # 생성기 실행
        LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Executing {current_gen.ai_request_type} wireframe generation for UI component '{ui_name}'")
        result = generator.generate(current_gen.retry_count > 0, current_gen.retry_count)
        
        # 결과 검증
        if not result or "result" not in result or not result["result"].get("html"):
            LogUtil.add_error_log(state, f"[UI_COMPONENTS_SUBGRAPH] No valid HTML result from wireframe generation for UI component '{ui_name}'")
            current_gen.retry_count += 1
            return state
        
        # HTML 결과 추출
        generated_html = result["result"]["html"]
        
        # ActionModel 생성 - UI 업데이트용
        ui_update_action = ActionModel(
            objectType="UI",
            type="update",
            ids={"uiId": current_gen.target_ui_component["id"]},
            args={"runTimeTemplateHtml": generated_html}
        )
        
        # 생성된 액션 저장
        current_gen.ui_replace_actions = [ui_update_action]
        
        LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Wireframe generation completed successfully for UI component '{ui_name}'. HTML length: {len(generated_html)} characters")
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[UI_COMPONENTS_SUBGRAPH] Failed to generate wireframe for UI component '{ui_name}'", e)
        if current_gen:
            current_gen.retry_count += 1

    return state

def postprocess_ui_components_generation(state: State) -> State:
    """
    UI 컴포넌트 생성 후처리 작업 수행
    - 생성된 UI replace actions를 ES 모델에 적용
    """
    current_gen = state.subgraphs.createUiComponentsModel.current_generation
    if not current_gen:
        LogUtil.add_info_log(state, "[UI_COMPONENTS_SUBGRAPH] No UI generation task currently being processed, skipping postprocessing")
        return state
        
    ui_name = current_gen.target_ui_component.get("name", "Unknown")
    LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Starting postprocessing for UI component '{ui_name}'")
    
    try:
        # 생성된 UI replace actions가 없으면 실패로 처리
        if not current_gen.ui_replace_actions:
            LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] No UI replace actions generated for component '{ui_name}', incrementing retry count")
            current_gen.retry_count += 1
            return state
        
        LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Applying {len(current_gen.ui_replace_actions)} UI replace actions for component '{ui_name}'")
        
        # 사용자 정보와 프로젝트 정보 준비
        user_info = {
            "uid": state.inputs.userInfo.get("uid", "")
        }
        information = state.inputs.information or {}
        
        # EsActionsUtil을 사용하여 액션 적용
        updated_es_value = EsActionsUtil.apply_actions(
            state.outputs.esValue,
            current_gen.ui_replace_actions,
            user_info,
            information
        )
        
        # 업데이트된 ES 값 저장
        state.outputs.esValue = updated_es_value
        current_gen.generation_complete = True
        
        LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Postprocessing completed successfully for UI component '{ui_name}'. Updated UI component with generated HTML wireframe")
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[UI_COMPONENTS_SUBGRAPH] Postprocessing failed for UI component '{ui_name}'", e)
        if current_gen:
            current_gen.retry_count += 1
            current_gen.ui_replace_actions = []

    return state

def validate_ui_components_generation(state: State) -> State:
    """
    UI 컴포넌트 생성 결과 검증 및 완료 처리
    - 생성 결과 검증
    - 완료 처리 또는 재시도 결정
    """
    current_gen = state.subgraphs.createUiComponentsModel.current_generation
    if not current_gen:
        LogUtil.add_info_log(state, "[UI_COMPONENTS_SUBGRAPH] No UI generation task currently being processed, skipping validation")
        return state
        
    ui_name = current_gen.target_ui_component.get("name", "Unknown")
    LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] Validating UI generation for component '{ui_name}'")
    
    try:
        # 생성 완료 확인
        if current_gen.generation_complete and not state.subgraphs.createUiComponentsModel.is_failed:
            # 변수 정리
            current_gen.target_ui_component = {}
            current_gen.ai_request_type = ""
            current_gen.ai_input_data = {}
            current_gen.ui_replace_actions = []

            # 완료된 작업을 완료 목록에 추가
            state.subgraphs.createUiComponentsModel.completed_generations.append(current_gen)
            # 현재 작업 초기화
            state.subgraphs.createUiComponentsModel.current_generation = None
            LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] UI generation completed successfully for component '{ui_name}'.")

        elif current_gen.retry_count > state.subgraphs.createUiComponentsModel.max_retry_count:
            # 최대 재시도 횟수 초과 시 실패로 처리하고 다음 작업으로 이동
            LogUtil.add_error_log(state, f"[UI_COMPONENTS_SUBGRAPH] Maximum retry count exceeded for UI component '{ui_name}' (retries: {current_gen.retry_count}). Moving to next task.")
            state.subgraphs.createUiComponentsModel.is_failed = True
            state.subgraphs.createUiComponentsModel.current_generation = None
        
        else:
            LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] UI generation not yet complete for component '{ui_name}', continuing process")
        
    except Exception as e:
        LogUtil.add_exception_object_log(state, f"[UI_COMPONENTS_SUBGRAPH] Validation failed for UI component '{ui_name}'", e)
        state.subgraphs.createUiComponentsModel.is_failed = True

    return state

# 단순 완료 처리를 위한 함수
def complete_processing(state: State) -> State:
    """
    UI Components 생성 프로세스 완료
    """
    
    try:

        state.outputs.lastCompletedRootGraphNode = ResumeNodes["ROOT_GRAPH"]["CREATE_UI_COMPONENTS"]
        state.outputs.lastCompletedSubGraphNode = ResumeNodes["CREATE_UI_COMPONENTS"]["COMPLETE"]
        state.outputs.currentProgressCount = state.outputs.currentProgressCount + 1
        JobUtil.update_job_to_firebase_fire_and_forget(state)

        # 완료된 작업 수 정보 로그
        completed_count = len(state.subgraphs.createUiComponentsModel.completed_generations)
        failed = state.subgraphs.createUiComponentsModel.is_failed
        
        if failed:
            LogUtil.add_error_log(state, f"[UI_COMPONENTS_SUBGRAPH] UI Components generation process completed with failures. Successfully processed: {completed_count} UI component tasks")
        else:
            LogUtil.add_info_log(state, f"[UI_COMPONENTS_SUBGRAPH] UI Components generation process completed successfully. Total processed: {completed_count} UI component tasks")
        
        if not failed:
            # 변수 정리
            subgraph_model = state.subgraphs.createUiComponentsModel
            subgraph_model.current_generation = None
            subgraph_model.completed_generations = []
            subgraph_model.pending_generations = []

    except Exception as e:
        LogUtil.add_exception_object_log(state, "[UI_COMPONENTS_SUBGRAPH] Failed during UI Components generation process completion", e)
        state.subgraphs.createUiComponentsModel.is_failed = True

    return state

# 라우팅 함수: 다음 단계 결정
def decide_next_step(state: State) -> str:
    """
    다음 실행할 단계 결정
    """
    try :

        if state.subgraphs.createUiComponentsModel.is_failed:
            return "complete"

        # 모든 작업이 완료되었으면 완료 상태로 이동
        if state.subgraphs.createUiComponentsModel.all_complete:
            return "complete"
        
        # 현재 처리 중인 작업이 없으면 다음 작업 선택
        if not state.subgraphs.createUiComponentsModel.current_generation:
            return "select_next"
        
        current_gen = state.subgraphs.createUiComponentsModel.current_generation

        # 실패 혹은 최대 재시도 횟수 초과 시 다음 가능한 작업으로 이동
        if current_gen.is_failed or current_gen.retry_count > state.subgraphs.createUiComponentsModel.max_retry_count:
            return "select_next"
        
        # 현재 작업이 완료되었으면 검증 단계로 이동
        if current_gen.generation_complete:
            return "validate"
        
        # 전처리로 인한 요약 정보가 없을 경우, 전처리 단계로 이동
        if not current_gen.ai_input_data or not current_gen.ai_request_type:
            return "preprocess"
        
        # 기본적으로 생성 실행 단계로 이동
        if not current_gen.ui_replace_actions:
            return "generate"
        
        # 생성된 UI Components가 있으면 후처리 단계로 이동
        return "postprocess"
    
    except Exception as e:
        LogUtil.add_exception_object_log(state, "[UI_COMPONENTS_SUBGRAPH] Failed during decide_next_step", e)
        state.subgraphs.createUiComponentsModel.is_failed = True
        return "complete"

# 서브그래프 생성 함수
def create_ui_components_subgraph() -> Callable:
    """
    UI Components 생성 서브그래프 생성
    """
    # 서브그래프 정의
    subgraph = StateGraph(State)
    
    # 노드 추가
    subgraph.add_node("prepare", prepare_ui_components_generation)
    subgraph.add_node("select_next", select_next_ui_components_generation)
    subgraph.add_node("preprocess", preprocess_ui_components_generation)
    subgraph.add_node("generate", generate_ui_components_generation)
    subgraph.add_node("postprocess", postprocess_ui_components_generation)
    subgraph.add_node("validate", validate_ui_components_generation)
    subgraph.add_node("complete", complete_processing)
    
    # 엣지 추가 (라우팅)
    subgraph.add_conditional_edges(START, resume_from_create_ui_components, {
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