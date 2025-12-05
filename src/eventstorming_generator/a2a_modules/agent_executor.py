"""
AgentExecutor 구현 모듈
이벤트 스토밍 생성 태스크를 처리합니다.
스트리밍 방식으로 Firebase watch를 통해 실시간 상태를 전달합니다.
"""

import asyncio
import json
import uuid
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
    TaskArtifactUpdateEvent,
    Artifact,
    TextPart,
    Message,
    Part,
    Role,
)

from ..utils.job_utils import JobRequestUtil, A2ASessionManager
from ..utils.logging_util import LoggingUtil


class EventStormingAgentExecutor(AgentExecutor):
    """
    이벤트 스토밍 생성 에이전트 실행기
    요구사항을 받아 이벤트 스토밍 다이어그램 생성을 처리합니다.
    
    현재 비스트리밍 방식으로 동작합니다 (링크만 반환 후 즉시 완료).
    스트리밍 방식은 _execute_streaming 메서드로 보존되어 있습니다.
    """
    
    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        """
        Task를 처리하는 메인 메서드
        비스트리밍 방식으로 작업 요청 후 링크만 반환하고 즉시 완료합니다.
        
        Args:
            context: 요청 컨텍스트 (사용자 메시지, task ID 등 포함)
            event_queue: 이벤트를 발행할 큐
        """
        task_id = context.task_id
        context_id = context.context_id
        
        LoggingUtil.debug("agent_executor", f"Task 수신: {task_id}")
        
        # 1. Task 상태를 WORKING으로 변경
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                status=TaskStatus(state=TaskState.working),
                final=False,
            )
        )
        
        # 2. 사용자 입력 가져오기 (requirements)
        requirements = context.get_user_input()
        LoggingUtil.debug("agent_executor", f"요구사항 수신: {requirements[:100]}..." if len(requirements) > 100 else f"요구사항 수신: {requirements}")
        
        if not requirements or not requirements.strip():
            # 입력이 없는 경우 에러 처리
            await self._send_error(
                task_id, context_id, event_queue,
                "이벤트 스토밍 생성을 위한 요구사항이 필요합니다."
            )
            return
        
        # 3. 비스트리밍 방식으로 작업 처리 (링크만 반환하고 즉시 완료)
        await self._execute_non_streaming(
            task_id, context_id, requirements, event_queue
        )
        
        LoggingUtil.debug("agent_executor", f"Task 완료: {task_id}")

    async def _execute_non_streaming(
        self,
        task_id: str,
        context_id: str,
        requirements: str,
        event_queue: EventQueue
    ) -> None:
        """
        비스트리밍 모드: 작업 요청 후 링크만 반환하고 즉시 완료
        
        A2A SDK의 TaskManager 동작 원리에 따라:
        1. TaskStatusUpdateEvent의 status.message 필드에 응답 메시지 포함
        2. 다음 이벤트(completed) 처리 시 이전 message가 task.history에 추가됨
        3. 클라이언트의 extract_result_from_task가 history에서 결과 추출
        """
        requirements_preview = requirements[:100] + "..." if len(requirements) > 100 else requirements
        
        # [LDVC] 프로세스 시작 로깅 - Intent: 비스트리밍 처리 시작
        LoggingUtil.debug(
            "agent_executor",
            f"[NON_STREAMING_START] Starting non-streaming execution | "
            f"task_id={task_id} | context_id={context_id} | "
            f"requirements_length={len(requirements)} | requirements_preview=\"{requirements_preview}\""
        )
        
        try:
            # 1. 작업 큐에 추가하고 job_id, link 획득
            LoggingUtil.debug(
                "agent_executor",
                f"[JOB_REQUEST] Submitting job request to work queue | task_id={task_id}"
            )
            
            job_id, link = JobRequestUtil.add_job_request_by_requirements(requirements)
            
            # [LDVC] 작업 요청 결과 로깅 - Reason: 작업 큐 추가 성공 여부 검증
            LoggingUtil.debug(
                "agent_executor",
                f"[JOB_REQUEST_SUCCESS] Job request added to work queue successfully | "
                f"task_id={task_id} | job_id={job_id} | link={link}"
            )
            
            # 2. 응답 메시지 생성
            response_text = (
                f"The event storming generation request has been added to the work queue. "
                f"Please refer to the following link to check the progress and results: {link}"
            )
            
            # 3. Message 객체 생성 (A2A 클라이언트가 task.history에서 추출할 수 있는 형식)
            message_id = str(uuid.uuid4())
            response_message = Message(
                message_id=message_id,
                role=Role.agent,
                parts=[
                    Part(root=TextPart(text=response_text))
                ],
                task_id=task_id,
                context_id=context_id,
            )
            
            # [LDVC] Message 객체 생성 로깅 - Reason: A2A 클라이언트 호환성 검증
            LoggingUtil.debug(
                "agent_executor",
                f"[MESSAGE_CREATED] A2A response message created | "
                f"task_id={task_id} | message_id={message_id} | role=agent | "
                f"response_text_length={len(response_text)}"
            )
            
            # 4. WORKING 상태로 변경하면서 message를 함께 전달
            #    이 message는 다음 이벤트 처리 시 task.history에 추가됨
            LoggingUtil.debug(
                "agent_executor",
                f"[A2A_EVENT] Sending TaskStatusUpdateEvent with message | "
                f"task_id={task_id} | state=working | final=False | "
                f"reason=\"Message will be added to task.history on next event\""
            )
            
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    task_id=task_id,
                    context_id=context_id,
                    status=TaskStatus(
                        state=TaskState.working,
                        message=response_message,
                    ),
                    final=False,
                )
            )
            
            # [LDVC] 이벤트 발행 성공 로깅
            LoggingUtil.debug(
                "agent_executor",
                f"[A2A_EVENT_SENT] Working status with message sent successfully | "
                f"task_id={task_id} | message_id={message_id}"
            )
            
            # 5. COMPLETED 상태로 변경
            #    이 이벤트가 처리될 때, 이전 status.message가 history에 추가됨
            LoggingUtil.debug(
                "agent_executor",
                f"[A2A_EVENT] Sending TaskStatusUpdateEvent for completion | "
                f"task_id={task_id} | state=completed | final=True | "
                f"reason=\"Previous message will be added to task.history now\""
            )
            
            await event_queue.enqueue_event(
                TaskStatusUpdateEvent(
                    task_id=task_id,
                    context_id=context_id,
                    status=TaskStatus(state=TaskState.completed),
                    final=True,
                )
            )
            
            # [LDVC] 프로세스 완료 로깅 - 전체 흐름 검증
            LoggingUtil.debug(
                "agent_executor",
                f"[NON_STREAMING_COMPLETE] Non-streaming execution completed successfully | "
                f"task_id={task_id} | job_id={job_id} | link={link} | "
                f"flow=\"job_request -> message_created -> working_event -> completed_event\""
            )
            
        except Exception as e:
            # [LDVC] 에러 로깅 - 디버깅을 위한 충분한 컨텍스트 제공
            LoggingUtil.exception(
                "agent_executor",
                f"[NON_STREAMING_ERROR] Non-streaming execution failed | "
                f"task_id={task_id} | context_id={context_id} | "
                f"error_type={type(e).__name__} | error_message={str(e)} | "
                f"requirements_preview=\"{requirements_preview}\"",
                e
            )
            await self._send_error(task_id, context_id, event_queue, str(e))

    async def _execute_streaming(
        self,
        task_id: str,
        context_id: str,
        requirements: str,
        event_queue: EventQueue
    ) -> None:
        """
        스트리밍 모드: Firebase watch를 통해 실시간 상태 전달
        """
        session_id = str(uuid.uuid4())
        session_manager = A2ASessionManager.instance()
        artifact_index = 0
        
        try:
            # A2A 세션 등록
            session_manager.register_session(session_id)
            LoggingUtil.debug("agent_executor", f"A2A 세션 등록: {session_id}")
            
            # JobRequestUtil의 스트리밍 로직 사용
            async for event in JobRequestUtil.add_job_request_with_streaming(requirements):
                event_type = event.get("type", "unknown")
                state = event.get("state", "unknown")
                
                # 이벤트 타입에 따라 Artifact 생성 및 발행
                content = self._create_event_content(event, event_type, state)
                
                is_final = event_type in ("completed", "failed", "error")
                
                # Artifact 발행
                chunk_artifact = Artifact(
                    artifact_id=str(uuid.uuid4()),
                    parts=[TextPart(text=json.dumps(content, ensure_ascii=False))],
                    name="event_storming_response",
                    index=artifact_index,
                )
                
                await event_queue.enqueue_event(
                    TaskArtifactUpdateEvent(
                        task_id=task_id,
                        context_id=context_id,
                        artifact=chunk_artifact,
                        last_chunk=is_final,
                    )
                )
                
                artifact_index += 1
                
                # 완료/실패 시 최종 상태 업데이트
                if event_type == "completed":
                    await event_queue.enqueue_event(
                        TaskStatusUpdateEvent(
                            task_id=task_id,
                            context_id=context_id,
                            status=TaskStatus(state=TaskState.completed),
                            final=True,
                        )
                    )
                    break
                    
                elif event_type in ("failed", "error"):
                    await event_queue.enqueue_event(
                        TaskStatusUpdateEvent(
                            task_id=task_id,
                            context_id=context_id,
                            status=TaskStatus(state=TaskState.failed),
                            final=True,
                        )
                    )
                    break
                    
        except Exception as e:
            LoggingUtil.exception("agent_executor", f"스트리밍 처리 오류: {task_id}", e)
            await self._send_error(task_id, context_id, event_queue, str(e))
            
        finally:
            # A2A 세션 해제
            session_manager.unregister_session(session_id)
            LoggingUtil.debug("agent_executor", f"A2A 세션 해제: {session_id}")

    def _create_event_content(self, event: dict, event_type: str, state: str) -> dict:
        """
        이벤트 타입에 따라 클라이언트에게 전달할 콘텐츠 생성
        """
        if event_type == "status_update":
            return {
                "type": event_type,
                "state": state,
                "job_id": event.get("job_id"),
                "link": event.get("link"),
                "message": event.get("message")
            }
        elif event_type == "log":
            log_data = event.get("log", {})
            return {
                "type": event_type,
                "level": log_data.get("level"),
                "message": log_data.get("message")
            }
        elif event_type == "progress":
            return {
                "type": event_type,
                "progress": event.get("progress"),
                "total": event.get("total"),
                "message": event.get("message")
            }
        elif event_type == "completed":
            return {
                "type": event_type,
                "state": state,
                "job_id": event.get("job_id"),
                "link": event.get("link"),
                "message": event.get("message")
            }
        elif event_type == "failed":
            return {
                "type": event_type,
                "state": state,
                "job_id": event.get("job_id"),
                "link": event.get("link"),
                "message": event.get("message")
            }
        elif event_type == "heartbeat":
            return {
                "type": event_type,
                "message": event.get("message")
            }
        elif event_type == "error":
            return {
                "type": event_type,
                "state": state,
                "message": event.get("message")
            }
        else:
            return {
                "type": event_type,
                "data": event
            }

    async def _send_error(
        self,
        task_id: str,
        context_id: str,
        event_queue: EventQueue,
        error_message: str
    ) -> None:
        """
        에러 메시지를 발행하고 Task를 실패 상태로 변경
        """
        error_artifact = Artifact(
            artifact_id=str(uuid.uuid4()),
            parts=[TextPart(text=json.dumps({
                "type": "error",
                "state": "failed",
                "message": error_message
            }, ensure_ascii=False))],
            name="error_response",
        )
        
        await event_queue.enqueue_event(
            TaskArtifactUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                artifact=error_artifact,
                last_chunk=True,
            )
        )
        
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                status=TaskStatus(state=TaskState.failed),
                final=True,
            )
        )

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        """
        Task 취소 처리
        
        Args:
            context: 요청 컨텍스트
            event_queue: 이벤트를 발행할 큐
        """
        task_id = context.task_id
        context_id = context.context_id
        
        LoggingUtil.debug("agent_executor", f"Task 취소 요청: {task_id}")
        
        # 취소 상태로 변경
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                status=TaskStatus(state=TaskState.canceled),
                final=True,
            )
        )
        
        LoggingUtil.debug("agent_executor", f"Task 취소됨: {task_id}")


if __name__ == "__main__":
    # 테스트: AgentExecutor 생성
    executor = EventStormingAgentExecutor()
    print("✅ EventStormingAgentExecutor 생성 성공!")
    print(f"📝 Executor 클래스: {executor.__class__.__name__}")

