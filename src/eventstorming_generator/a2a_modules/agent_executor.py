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
)

from ..utils.job_utils import JobRequestUtil, A2ASessionManager
from ..utils.logging_util import LoggingUtil


class EventStormingAgentExecutor(AgentExecutor):
    """
    이벤트 스토밍 생성 에이전트 실행기
    요구사항을 받아 이벤트 스토밍 다이어그램 생성을 처리합니다.
    스트리밍 방식으로만 동작합니다.
    """
    
    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        """
        Task를 처리하는 메인 메서드
        스트리밍 방식으로 Firebase watch를 통해 실시간 상태를 전달합니다.
        
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
        
        # 3. 스트리밍 방식으로 작업 처리
        await self._execute_streaming(
            task_id, context_id, requirements, event_queue
        )
        
        LoggingUtil.debug("agent_executor", f"Task 완료: {task_id}")

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

