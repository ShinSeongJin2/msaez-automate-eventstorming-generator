# server/agent_executor.py
"""
AgentExecutor 구현 모듈
실제 태스크 처리 로직을 구현합니다.
- 비스트리밍: 한 번에 전체 결과 반환
- 스트리밍: 여러 청크로 나누어 순차적으로 반환
"""

import asyncio
import uuid
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.types import (
    Task,
    TaskState,
    TaskStatus,
    TaskStatusUpdateEvent,
    TaskArtifactUpdateEvent,
    Artifact,
    TextPart,
    Message,
    Role,
)


class GreetingAgentExecutor(AgentExecutor):
    """
    인사 에이전트 실행기
    사용자의 이름을 받아 인사 메시지를 생성합니다.
    스트리밍/비스트리밍 요청 모두 지원합니다.
    """
    
    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        """
        Task를 처리하는 메인 메서드
        스트리밍 요청의 경우 여러 청크로 나누어 응답합니다.
        
        Args:
            context: 요청 컨텍스트 (사용자 메시지, task ID 등 포함)
            event_queue: 이벤트를 발행할 큐
        """
        task_id = context.task_id
        context_id = context.context_id
        
        print(f"📥 Task 수신: {task_id}")
        
        # 1. Task 상태를 WORKING으로 변경
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                status=TaskStatus(state=TaskState.working),
                final=False,
            )
        )
        
        # 2. 사용자 입력 가져오기
        user_input = context.get_user_input()
        print(f"📝 사용자 입력: {user_input}")
        
        # 스트리밍 모드로 응답 (여러 청크로 나누어 전송)
        # - 비스트리밍 클라이언트: 모든 청크가 처리된 후 최종 결과 수신
        # - 스트리밍 클라이언트: 각 청크를 실시간으로 수신
        await self._execute_streaming(
            task_id, context_id, user_input, event_queue
        )
        
        print(f"✅ Task 완료: {task_id}")

    async def _execute_non_streaming(
        self,
        task_id: str,
        context_id: str,
        user_input: str,
        event_queue: EventQueue
    ) -> None:
        """
        비스트리밍 모드: 전체 응답을 한 번에 반환
        """
        # 작업 시뮬레이션
        await asyncio.sleep(1)
        
        # 인사 메시지 생성
        if user_input.strip():
            greeting_message = f"안녕하세요, {user_input}님! 반갑습니다. 🎉"
        else:
            greeting_message = "안녕하세요! 반갑습니다. 🎉"
        
        print(f"💬 생성된 메시지: {greeting_message}")
        
        # 결과를 Artifact로 한 번에 발행
        result_artifact = Artifact(
            artifact_id=str(uuid.uuid4()),
            parts=[TextPart(text=greeting_message)],
            name="greeting_response",
        )
        
        await event_queue.enqueue_event(
            TaskArtifactUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                artifact=result_artifact,
                last_chunk=True,
            )
        )
        
        # Task 상태를 COMPLETED로 변경
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                status=TaskStatus(state=TaskState.completed),
                final=True,
            )
        )

    async def _execute_streaming(
        self,
        task_id: str,
        context_id: str,
        user_input: str,
        event_queue: EventQueue
    ) -> None:
        """
        스트리밍 모드: 응답을 여러 청크로 나누어 순차적으로 반환
        
        실제 LLM 스트리밍처럼 단어 또는 문장 단위로 응답을 전송합니다.
        """
        # 스트리밍할 메시지 청크들 생성
        if user_input.strip():
            chunks = [
                f"안녕하세요, ",
                f"{user_input}",
                f"님! ",
                f"반갑습니다. ",
                f"🎉\n",
                f"오늘도 ",
                f"좋은 ",
                f"하루 ",
                f"되세요!"
            ]
        else:
            chunks = [
                "안녕하세요! ",
                "반갑습니다. ",
                "🎉\n",
                "좋은 ",
                "하루 ",
                "되세요!"
            ]
        
        print(f"📤 스트리밍 시작: {len(chunks)}개 청크")
        
        # 각 청크를 순차적으로 스트리밍
        for i, chunk in enumerate(chunks):
            is_last = (i == len(chunks) - 1)
            
            # 청크별 Artifact 생성
            chunk_artifact = Artifact(
                artifact_id=str(uuid.uuid4()),
                parts=[TextPart(text=chunk)],
                name="greeting_response",
                index=i,  # 청크 순서
            )
            
            await event_queue.enqueue_event(
                TaskArtifactUpdateEvent(
                    task_id=task_id,
                    context_id=context_id,
                    artifact=chunk_artifact,
                    last_chunk=is_last,  # 마지막 청크 여부
                )
            )
            
            print(f"  📦 청크 {i+1}/{len(chunks)}: {repr(chunk)}")
            
            # 실제 LLM 응답처럼 약간의 지연 추가
            await asyncio.sleep(0.3)
        
        # Task 상태를 COMPLETED로 변경
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                status=TaskStatus(state=TaskState.completed),
                final=True,
            )
        )
        
        print(f"📤 스트리밍 완료")

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
        
        print(f"🚫 Task 취소 요청: {task_id}")
        
        # 취소 상태로 변경
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                status=TaskStatus(state=TaskState.canceled),
                final=True,
            )
        )
        
        print(f"❌ Task 취소됨: {task_id}")


if __name__ == "__main__":
    # 테스트: AgentExecutor 생성
    executor = GreetingAgentExecutor()
    print("✅ GreetingAgentExecutor 생성 성공!")
    print(f"📝 Executor 클래스: {executor.__class__.__name__}")