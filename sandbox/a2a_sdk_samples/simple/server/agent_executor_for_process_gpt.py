# server/agent_executor_for_process_gpt.py
"""
AgentExecutor 구현 모듈 (Process GPT용)
a2a_client.py의 send_message_to_agent에 최적화된 구현입니다.

차이점:
- 스트리밍이 아닌 blocking 요청에 최적화
- task.history를 통해 결과 반환 (TaskStatus.message 사용)
- artifacts가 아닌 message를 통해 응답 전달

핵심 원리:
- A2A SDK의 TaskManager는 새로운 TaskStatusUpdateEvent가 처리될 때
  이전 task.status.message를 task.history에 추가함
- 따라서 메시지가 포함된 이벤트를 보낸 후, 추가 이벤트를 보내야 history에 추가됨
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
    Message,
    Part,
    TextPart,
    Role,
)


class GreetingAgentExecutorForProcessGPT(AgentExecutor):
    """
    인사 에이전트 실행기 (Process GPT용)
    
    a2a_client.py의 send_message_to_agent를 통해 호출될 때,
    task.history에서 결과를 추출할 수 있도록 최적화되었습니다.
    
    주요 변경점:
    - TaskArtifactUpdateEvent 대신 TaskStatusUpdateEvent.status.message 사용
    - blocking 요청에 적합한 비스트리밍 방식
    - 두 단계 이벤트 발행: working(with message) -> completed
    """
    
    async def execute(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        """
        Task를 처리하는 메인 메서드
        
        비스트리밍 방식으로 한 번에 결과를 반환합니다.
        결과는 TaskStatus.message를 통해 task.history에 추가됩니다.
        
        Args:
            context: 요청 컨텍스트 (사용자 메시지, task ID 등 포함)
            event_queue: 이벤트를 발행할 큐
        """
        task_id = context.task_id
        context_id = context.context_id
        
        print(f"📥 Task 수신: {task_id}")
        
        # 1. Task 상태를 WORKING으로 변경 (메시지 없이)
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
        
        # 3. 비스트리밍 방식으로 결과 반환 (message를 통해)
        await self._execute_with_message(
            task_id, context_id, user_input, event_queue
        )
        
        print(f"✅ Task 완료: {task_id}")

    async def _execute_with_message(
        self,
        task_id: str,
        context_id: str,
        user_input: str,
        event_queue: EventQueue
    ) -> None:
        """
        Message를 통해 결과를 반환하는 방식
        
        A2A SDK의 TaskManager 동작 원리:
        1. TaskStatusUpdateEvent가 처리될 때, 현재 task.status.message가 있으면
           그것을 task.history에 추가한 후 새로운 status로 교체함
        2. 따라서 메시지를 history에 추가하려면:
           - 먼저 message가 포함된 이벤트를 보냄 (working 상태)
           - 그 다음 추가 이벤트를 보냄 (completed 상태)
           -> 두 번째 이벤트 처리 시 첫 번째의 message가 history에 추가됨
        """
        # 작업 시뮬레이션
        await asyncio.sleep(1)
        
        # 인사 메시지 생성
        if user_input.strip():
            greeting_message = f"안녕하세요, {user_input}님! 반갑습니다. 🎉\n오늘도 좋은 하루 되세요!"
        else:
            greeting_message = "안녕하세요! 반갑습니다. 🎉\n좋은 하루 되세요!"
        
        print(f"💬 생성된 메시지: {greeting_message}")
        
        # Message 객체 생성
        # a2a_client.py의 extract_result_from_task가 이해할 수 있는 형식
        response_message = Message(
            message_id=str(uuid.uuid4()),
            role=Role.agent,  # agent 역할로 응답 (user가 아닌 것만 결과로 추출됨)
            parts=[
                Part(root=TextPart(text=greeting_message))
            ],
            task_id=task_id,
            context_id=context_id,
        )
        
        # 단계 1: WORKING 상태로 변경하면서 message를 함께 전달
        # 이 message는 다음 이벤트 처리 시 task.history에 추가됨
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                status=TaskStatus(
                    state=TaskState.working,
                    message=response_message,  # 핵심: message 필드 사용
                ),
                final=False,
            )
        )
        
        print(f"📤 응답 메시지 전송 (status.message)")
        
        # 단계 2: COMPLETED 상태로 변경
        # 이 이벤트가 처리될 때, 이전 status.message가 history에 추가됨
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                status=TaskStatus(state=TaskState.completed),
                final=True,
            )
        )
        
        print(f"📤 완료 상태 전송 (message가 history에 추가됨)")

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
    executor = GreetingAgentExecutorForProcessGPT()
    print("✅ GreetingAgentExecutorForProcessGPT 생성 성공!")
    print(f"📝 Executor 클래스: {executor.__class__.__name__}")
