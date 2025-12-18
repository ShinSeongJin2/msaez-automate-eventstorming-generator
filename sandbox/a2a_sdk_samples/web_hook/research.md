이제 충분한 정보를 수집했습니다. 조사 결과를 정리해 드리겠습니다.

## A2A Push Notifications 스펙 및 Python SDK 구현 가이드

### Push Notifications 스펙 존재 여부

네, **Push Notifications는 A2A 프로토콜의 공식 스펙에 정의된 Capability입니다.** **Agent가 이 기능을 지원하는 경우 `AgentCard.capabilities.pushNotifications`를 `true`로 설정해야 합니다.** [1]

---

## Push Notifications 개요

Push Notifications(Webhooks)는 A2A 프로토콜에서 태스크 상태 모니터링을 위한 세 가지 메커니즘 중 하나입니다:

| 방식                     | 설명                               | 적합한 사용 사례                                       |
| ---------------------- | -------------------------------- | ----------------------------------------------- |
| **Polling**            | 주기적으로 `GetTask` 호출               | 간단한 통합, 방화벽 뒤의 클라이언트                            |
| **Streaming**          | 실시간 이벤트 스트림 유지                   | 대화형 앱, 실시간 대시보드                                 |
| **Push Notifications** | Agent가 Webhook URL로 HTTP POST 전송 | **매우 긴 실행 시간 (분, 시간, 또는 며칠)**, 지속 연결 불가능한 클라이언트 |

**For very long-running tasks (e.g., lasting minutes, hours, or even days) or when clients cannot or prefer not to maintain persistent connections (like mobile clients or serverless functions)** [2]

---

## PushNotificationConfig 스펙 상세

### 데이터 구조 (Section 4.3.1)

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `id` | `string` | No | Push notification의 고유 식별자 (UUID) |
| `url` | `string` | **Yes** | 알림을 전송할 Webhook URL |
| `token` | `string` | No | 해당 task/session에 고유한 인증 토큰 |

[1]

### 관련 API 작업 (Section 3.1.7)

**Set or Update Push Notification Config** 작업:
- **메서드**: `tasks/pushNotificationConfig/set`
- **입력**: `TaskPushNotificationConfig` 객체
- **출력**: 생성된 `PushNotificationConfig` (할당된 ID 포함)
- **에러**: `PushNotificationNotSupportedError`, `TaskNotFoundError`

**The operation MUST establish a webhook endpoint for task update notifications** [1]

---

## Webhook 요청 형식

태스크 업데이트 시 Agent가 전송하는 HTTP 요청:

```http
POST {webhook_url}
Authorization: {authentication_scheme} {credentials}
Content-Type: application/json

{
  /* StreamResponse 객체 - 다음 중 하나: */
  "task": { /* Task 객체 */ },
  "message": { /* Message 객체 */ },
  "statusUpdate": { /* TaskStatusUpdateEvent 객체 */ },
  "artifactUpdate": { /* TaskArtifactUpdateEvent 객체 */ }
}
```

[1]

---

## 보안 요구사항

### 서버 (Agent) 요구사항
- Private IP 대역 거부 (127.0.0.0/8, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
- localhost 및 link-local 주소 거부
- URL allowlist 구현 권장

### 클라이언트 (Webhook Receiver) 요구사항
- 제공된 인증 자격 증명으로 webhook 진위 검증 **필수**
- payload의 task ID가 생성한 task와 일치하는지 확인 **권장**
- HTTP 2xx 상태 코드로 수신 확인 응답 **필수**
- 중복 전송 대비 멱등성 처리 **권장**
- rate limiting 구현 **권장**
- HTTPS 엔드포인트 사용 **권장**

[1]

---

## Python a2a-sdk 구현 가이드

현재 Python a2a-sdk에 대한 구체적인 Push Notification 구현 예제는 공식 문서에서 찾기 어렵습니다. 그러나 JavaScript SDK (`@a2a-js/sdk`)의 구현 패턴을 참고하여 Python에서 구현할 수 있습니다. [2]

### 서버 측 구현 (Agent)

```python
# 개념적 구현 예시 (a2a-sdk 기반)
from a2a.types import (
    AgentCard,
    AgentCapabilities,
    PushNotificationConfig,
    Task,
    TaskStatusUpdateEvent
)
import httpx

# 1. AgentCard에 pushNotifications 활성화
agent_card = AgentCard(
    name="LongRunningAgent",
    capabilities=AgentCapabilities(
        pushNotifications=True,  # Push Notifications 활성화
        streaming=True,
        stateTransitionHistory=True
    ),
    # ... 기타 설정
)

# 2. Push Notification 저장소 (메모리 또는 DB)
class PushNotificationStore:
    def __init__(self):
        self._configs: dict[str, list[PushNotificationConfig]] = {}
    
    def set_config(self, task_id: str, config: PushNotificationConfig):
        if task_id not in self._configs:
            self._configs[task_id] = []
        self._configs[task_id].append(config)
    
    def get_configs(self, task_id: str) -> list[PushNotificationConfig]:
        return self._configs.get(task_id, [])

# 3. Push Notification Sender
class PushNotificationSender:
    def __init__(self, store: PushNotificationStore, timeout: int = 5000):
        self.store = store
        self.timeout = timeout / 1000
    
    async def send_notification(self, task_id: str, event: TaskStatusUpdateEvent):
        configs = self.store.get_configs(task_id)
        
        async with httpx.AsyncClient() as client:
            for config in configs:
                headers = {"Content-Type": "application/json"}
                
                # 인증 토큰이 있으면 헤더에 추가
                if config.token:
                    headers["X-A2A-Notification-Token"] = config.token
                
                try:
                    await client.post(
                        config.url,
                        json=event.model_dump(),
                        headers=headers,
                        timeout=self.timeout
                    )
                except Exception as e:
                    print(f"Failed to send notification: {e}")

# 4. 장시간 태스크 처리 시 알림 전송
async def handle_long_running_task(task_id: str, sender: PushNotificationSender):
    # 태스크 처리 로직...
    # 완료 시 알림 전송
    completion_event = TaskStatusUpdateEvent(
        taskId=task_id,
        status={"state": "completed", "timestamp": "..."},
        final=True
    )
    await sender.send_notification(task_id, completion_event)
```

### 클라이언트 측 구현 (Webhook 수신)

```python
from fastapi import FastAPI, Request, HTTPException
from a2a.types import StreamResponse

app = FastAPI()

# Webhook 엔드포인트 설정
@app.post("/webhook/a2a-notification")
async def receive_notification(request: Request):
    # 1. 토큰 검증
    token = request.headers.get("X-A2A-Notification-Token")
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    
    # 2. Payload 파싱
    body = await request.json()
    
    # 3. 이벤트 처리
    if "statusUpdate" in body:
        status = body["statusUpdate"]
        if status.get("status", {}).get("state") == "completed":
            print(f"Task {status['taskId']} completed!")
            # 결과 처리 로직
    
    elif "task" in body:
        task = body["task"]
        print(f"Received task update: {task}")
    
    # 4. 성공 응답 (2xx 필수)
    return {"status": "received"}

def verify_token(token: str) -> bool:
    # 토큰 검증 로직
    return token == "expected_token"
```

### 클라이언트에서 Push Notification 설정

```python
from a2a.client import A2AClient
from a2a.types import PushNotificationConfig

async def setup_push_notification():
    client = A2AClient(base_url="https://agent.example.com")
    
    # 메시지 전송 후 태스크 생성
    response = await client.send_message(message="장시간 처리 요청")
    task_id = response.task.id
    
    # Push Notification 설정
    config = PushNotificationConfig(
        url="https://my-server.com/webhook/a2a-notification",
        token="my-secret-token-123"
    )
    
    # 서버에 Webhook 설정 요청
    await client.set_push_notification_config(
        task_id=task_id,
        config=config
    )
    
    print(f"Push notification configured for task {task_id}")
```

---

## 주의사항

1. **Python SDK 상태**: 현재 Google의 공식 Python a2a-sdk에서 Push Notification 관련 구체적인 구현 예제나 헬퍼 클래스가 문서화되어 있지 않을 수 있습니다. SDK 소스 코드를 직접 확인하거나, 위 스펙을 바탕으로 직접 구현해야 할 수 있습니다.

2. **JavaScript SDK 참고**: `@a2a-js/sdk`에는 `InMemoryPushNotificationStore`, `DefaultPushNotificationSender` 등의 헬퍼 클래스가 제공됩니다. Python 구현 시 이를 참고할 수 있습니다. [2]

3. **AgentCard 확인**: Push Notification을 사용하기 전에 대상 Agent의 `AgentCard.capabilities.pushNotifications`가 `true`인지 확인해야 합니다.

Citations:
[1] https://a2a-protocol.org/latest/specification/
[2] https://www.npmjs.com/package/@a2a-js/sdk?activeTab=dependencies
