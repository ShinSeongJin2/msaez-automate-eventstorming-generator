# A2A Webhook + HITL (Human-in-the-Loop) 샘플

A2A SDK의 Push Notification(Webhook)과 Human-in-the-Loop 기능을 활용한 샘플 코드입니다.

## 개요

이 샘플은 두 가지 핵심 기능을 보여줍니다:

1. **Webhook (Push Notification)**: 장시간 실행되는 태스크 완료 시 클라이언트에 알림
2. **Human-in-the-Loop (HITL)**: 작업 중 사용자 승인이 필요할 때 `input_required` 상태로 전환

### HITL 워크플로우

```
┌─────────────┐                                    ┌─────────────┐
│   Client    │  1. "예산 승인 요청" 메시지 전송     │   Server    │
│             │ ──────────────────────────────────▶│             │
│             │                                    │             │
│             │  2. 즉시 응답 (Task 생성됨)          │             │
│             │ ◀──────────────────────────────────│             │
│             │                                    │             │
│  Webhook    │  3. 🔔 input_required 알림          │  "예산" 키워드│
│  Receiver   │ ◀──────────────────────────────────│   감지됨     │
│  (9000)     │     "추가 확인이 필요합니다!"        │             │
│             │                                    │             │
│             │  4. 사용자 응답: "승인합니다"        │             │
│   (Mock)    │ ──────────────────────────────────▶│   작업 재개  │
│             │     (같은 task_id로)               │             │
│             │                                    │             │
│  Webhook    │  5. ✅ completed 알림               │             │
│  Receiver   │ ◀──────────────────────────────────│  작업 완료   │
└─────────────┘                                    └─────────────┘
```

### HITL 트리거 키워드

다음 키워드가 메시지에 포함되면 `input_required` 상태가 트리거됩니다:

| 한국어 | 영어 |
|--------|------|
| 승인 | approval |
| 확인 | confirm |
| 예산 | budget |
| - | hitl |
| - | human |

## 파일 구조

```
web_hook/
├── server/
│   ├── agent_card.py       # HITL + Webhook 지원 AgentCard
│   ├── agent_executor.py   # HITLDemoAgentExecutor (input_required 처리)
│   └── server.py           # HITL + Push Notification 서버
├── client/
│   ├── webhook_receiver.py # HITL 상태 감지 Webhook 수신 서버
│   └── client.py           # HITL Mock 응답 자동화 클라이언트
├── logger_config.py        # 로깅 설정
└── README.md
```

## 실행 방법

### 1. 서버 실행

터미널 1에서:

```bash
cd sandbox/a2a_sdk_samples/web_hook
uv run python -m server.server --port 8000
```

옵션:
- `--port`: 서버 포트 (기본: 8000)
- `--task-duration`: 태스크 처리 시간(초) (기본: 3)
- `--hitl-keywords`: HITL 트리거 키워드 (공백 구분)

### 2. 클라이언트 실행

터미널 2에서:

```bash
# HITL 트리거 메시지 (자동 승인)
uv run python -m client.client --message "예산 승인이 필요합니다"

# 일반 메시지 (HITL 없이 바로 완료)
uv run python -m client.client --message "데이터 처리 요청"

# Mock 모드 변경 (거부)
uv run python -m client.client --message "예산 확인 요청" --mock-mode reject
```

옵션:
- `--agent-url`: A2A 서버 URL (기본: http://localhost:8000)
- `--message`: 전송할 메시지
- `--webhook-port`: Webhook 수신 포트 (기본: 9000)
- `--mock-mode`: HITL 응답 모드 (`auto`, `approve`, `reject`, `custom`)
- `--custom-response`: 커스텀 응답 (mock-mode=custom일 때)

## 핵심 A2A SDK 컴포넌트

### HITL 상태 (`TaskState.input_required`)

```python
from a2a.types import TaskState, TaskStatus, TaskStatusUpdateEvent

# input_required 상태로 전환
await event_queue.enqueue_event(
    TaskStatusUpdateEvent(
        task_id=task_id,
        context_id=context_id,
        status=TaskStatus(
            state=TaskState.input_required,  # HITL 상태
            message=response_message,         # 사용자에게 보낼 메시지
        ),
        final=True,  # 현재 실행은 종료
    )
)
```

### 작업 재개 (HITL 응답 처리)

```python
# 같은 task_id로 메시지를 다시 보내면 작업이 재개됩니다
hitl_request = SendMessageRequest(
    params=MessageSendParams(
        message=Message(
            message_id=str(uuid.uuid4()),
            parts=[Part(root=TextPart(text="승인합니다"))],
            role=Role.user,
            task_id=existing_task_id,      # 기존 task_id 사용
            context_id=existing_context_id,
        ),
        configuration=configuration,
    )
)
await client.send_message(hitl_request)
```

### Webhook 수신 서버에서 HITL 감지

```python
from webhook_receiver import TaskNotificationType

# 알림 유형 확인
if notification.notification_type == TaskNotificationType.INPUT_REQUIRED:
    print(f"🔔 HITL 감지: {notification.input_prompt}")
    # 사용자 입력 요청 또는 자동 응답 전송
```

## 코드 예시

### 서버: HITL 트리거 로직

```python
class HITLDemoAgentExecutor(AgentExecutor):
    def _should_require_input(self, user_input: str) -> bool:
        """HITL 키워드 감지"""
        for keyword in self.hitl_keywords:
            if keyword.lower() in user_input.lower():
                return True
        return False
    
    async def _trigger_hitl(self, task_id, context_id, event_queue):
        """input_required 상태로 전환"""
        await event_queue.enqueue_event(
            TaskStatusUpdateEvent(
                task_id=task_id,
                context_id=context_id,
                status=TaskStatus(
                    state=TaskState.input_required,
                    message=Message(
                        parts=[Part(root=TextPart(text="추가 확인이 필요합니다!"))]
                    ),
                ),
                final=True,
            )
        )
```

### 클라이언트: HITL 자동 처리

```python
class A2AHITLClient:
    async def send_with_hitl_support(self, message: str):
        while hitl_iteration < max_iterations:
            notification = await self._webhook_receiver.wait_for_notification()
            
            if notification.notification_type == TaskNotificationType.INPUT_REQUIRED:
                # Mock 사용자 응답 생성
                mock_response = await self.mock_responder.get_response(
                    notification.input_prompt
                )
                
                # 같은 task_id로 응답 전송
                await client.send_message(
                    self._create_message_request(
                        message=mock_response,
                        task_id=notification.task_id,
                        context_id=notification.context_id,
                    )
                )
            
            elif notification.notification_type == TaskNotificationType.COMPLETED:
                return {"status": "completed", "result": notification.result_text}
```

## 예상 출력

### 서버 로그

```
🚀 A2A HITL + Webhook Demo Server
============================================================
📍 Server URL: http://localhost:8000
📄 Agent Card: http://localhost:8000/.well-known/agent.json

🔑 HITL Trigger Keywords:
   - approval
   - 승인
   - confirm
   - 확인
   - budget
   - 예산

💡 Tip: Send a message containing any keyword above to trigger HITL
============================================================

INFO | Task execution STARTED | task_id=abc-123 | user_input=예산 승인 요청
INFO | HITL TRIGGERED - Requesting user input | task_id=abc-123
INFO | State transition: WORKING -> INPUT_REQUIRED
...
INFO | HITL RESPONSE received - Resuming task | user_response=approve
INFO | State transition: INPUT_REQUIRED -> WORKING
INFO | State transition: WORKING -> COMPLETED
```

### 클라이언트 로그

```
============================================================
🚀 A2A HITL 클라이언트 시작
============================================================
에이전트 URL: http://localhost:8000
메시지: 예산 승인이 필요합니다
Mock 모드: auto
============================================================

INFO | HITL workflow STARTED
INFO | HITL detected (iteration 1) | prompt=⏸️ 추가 확인이 필요합니다!
INFO | Simulating user input delay: 2.0s
INFO | Mock user response generated | response=approve - 자동 승인 (Mock Response)
INFO | Sending HITL response | task_id=abc-123
INFO | HITL workflow COMPLETED successfully

============================================================
📋 HITL 워크플로우 결과
============================================================
상태: completed
Task ID: abc-123
HITL 반복: 1회
총 소요 시간: 8.45초

결과:
🎉 HITL 작업이 완료되었습니다!

원본 요청: 예산 승인이 필요합니다
사용자 응답: approve - 자동 승인 (Mock Response)
승인 상태: ✅ 승인됨
처리 결과: 성공적으로 완료됨
============================================================
```

## 주의사항

1. **HITL 키워드**: 메시지에 키워드가 포함되어야만 HITL이 트리거됩니다.
2. **Task ID 재사용**: HITL 응답 시 반드시 같은 `task_id`를 사용해야 합니다.
3. **Webhook 필수**: HITL 알림을 받으려면 Webhook이 설정되어 있어야 합니다.
4. **타임아웃**: 실제 환경에서는 HITL 대기 타임아웃을 적절히 설정하세요.
5. **보안**: 프로덕션에서는 HTTPS와 토큰 검증을 필수로 적용하세요.

## 실제 환경에서의 HITL 구현

이 샘플에서는 Mock 응답을 사용하지만, 실제 환경에서는:

```python
# 1. UI를 통한 사용자 입력
user_response = await show_approval_dialog(notification.input_prompt)

# 2. 이메일/Slack 등 외부 시스템 연동
await send_approval_request_email(notification)
user_response = await wait_for_email_response()

# 3. 관리자 대시보드 연동
await notify_admin_dashboard(notification)
user_response = await wait_for_admin_approval()
```
