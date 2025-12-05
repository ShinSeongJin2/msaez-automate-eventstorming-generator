import asyncio
import uuid
import logging
from typing import Any, Dict, Optional, List

import httpx
from a2a.client import A2AClient
from a2a.types import (
    SendMessageRequest, 
    MessageSendParams, 
    MessageSendConfiguration,
    Message,
    TextPart,
    Role,
    Part
)

logger = logging.getLogger(__name__)


class A2AClientManager:
    """A2A 클라이언트 관리 클래스"""
    
    def __init__(self, timeout: int = 60):
        self.timeout = timeout
        self._client: Optional[A2AClient] = None
        self._httpx_client: Optional[httpx.AsyncClient] = None
    
    async def __aenter__(self):
        """비동기 컨텍스트 매니저 진입"""
        self._httpx_client = httpx.AsyncClient(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """비동기 컨텍스트 매니저 종료"""
        if self._httpx_client:
            await self._httpx_client.aclose()
    
    def create_client(self, agent_endpoint: str) -> A2AClient:
        """A2A 클라이언트 생성"""
        if not self._httpx_client:
            raise RuntimeError("Client manager not initialized. Use async context manager.")
        
        self._client = A2AClient(httpx_client=self._httpx_client, url=agent_endpoint)
        return self._client
    
    def create_message_request(self, message: str) -> SendMessageRequest:
        """메시지 요청 생성"""
        # Create a Message object from the string message
        a2a_message = Message(
            message_id=str(uuid.uuid4()),
            parts=[
                Part(root=TextPart(
                    text=message,
                    kind="text"
                ))
            ],
            role=Role.user
        )
        
        # Create a SendMessageRequest (non-streaming)
        return SendMessageRequest(
            id=str(uuid.uuid4()),
            params=MessageSendParams(
                message=a2a_message,
                configuration=MessageSendConfiguration(
                    acceptedOutputModes=["text"],  # Accept text output
                    blocking=True,  # Blocking request
                )
            )
        )
    
    async def send_message(self, agent_endpoint: str, message: str) -> Any:
        """메시지 전송"""
        client = self.create_client(agent_endpoint)
        request = self.create_message_request(message)
        
        try:
            response = await client.send_message(request)
            return response
        except httpx.ConnectError as e:
            logger.error(f"Connection error: {e}. Is the A2A agent running at {agent_endpoint}?")
            raise
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            raise

async def send_message_to_agent(agent_endpoint: str, message: str) -> Dict[str, Any]:
    """클라이언트 매니저를 사용하여 에이전트에 메시지 전송"""
    async with A2AClientManager() as client_manager:
        try:
            response = await client_manager.send_message(agent_endpoint, message)
            
            # 응답에서 결과 추출
            if response and response.root and response.root.result:
                task = response.root.result
                result = extract_result_from_task(task)
                print(f"🔍 결과: {result}")
                return result
            else:
                return {"result": "No response from agent", "status": "completed"}
                
        except Exception as e:
            logger.error(f"Failed to send message to agent: {e}")
            raise

def extract_result_from_task(task: Any) -> Dict[str, Any]:
    """태스크에서 결과 추출"""
    history_compact: List[Dict[str, Any]] = []
    try:
        if task is not None and getattr(task, 'history', None):
            for m in task.history:
                try:
                    role_val = getattr(m, 'role', None)
                    role_name = role_val.value if hasattr(role_val, 'value') else str(role_val)
                except Exception:
                    role_name = None
                texts: List[str] = []
                try:
                    for p in getattr(m, 'parts', []) or []:
                        root = getattr(p, 'root', None)
                        if isinstance(root, TextPart) and getattr(root, 'text', None):
                            texts.append(root.text)
                except Exception:
                    pass
                history_compact.append({
                    'role': role_name,
                    'text': "".join(texts) if texts else None,
                })
    except Exception:
        history_compact = []
    
    result_text = ""
    for m in history_compact:
        if m['role'] != "user":
            result_text += m['text']

    return {
        "result": result_text or "Task completed",
        "status": "completed",
        "task_id": getattr(task, 'id', None)
    }

if __name__ == "__main__":
    asyncio.run(send_message_to_agent("http://34.64.136.142", """
도서관의 도서 관리와 대출/반납을 통합적으로 관리하는 화면을 만들려고 해.

'도서 관리' 화면에서는 새로운 도서를 등록하고 현재 보유한 도서들의 상태를 관리할 수 있어야 해.
도서 등록 시에는 도서명, ISBN, 저자, 출판사, 카테고리 정보를 입력받아야 해.
ISBN은 13자리 숫자여야 하고 중복 확인이 필요해. 카테고리는 소설/비소설/학술/잡지 중에서 선택할 수 있어야 해.
등록된 도서는 처음에 '대출가능' 상태가 되고, 이후 대출/반납 상황에 따라 '대출중', '예약중' 상태로 자동으로 변경되어야 해.
도서가 훼손되거나 분실된 경우 '폐기' 처리가 가능해야 하며, 폐기된 도서는 더 이상 대출이 불가능해야 해.

'대출/반납' 화면에서는 회원이 도서를 대출하고 반납하는 것을 관리할 수 있어야 해.
대출 신청 시에는 회원번호와 이름으로 회원을 확인하고, 대출할 도서를 선택해야 해. 도서는 도서명이나 ISBN으로 검색할 수 있어야 해.
대출 기간은 7일/14일/30일 중에서 선택할 수 있어.
만약 대출하려는 도서가 이미 대출 중이라면, 예약 신청이 가능해야 해.
대출이 완료되면 해당 도서의 상태는 자동으로 '대출중'으로 변경되어야 해.

대출 현황 화면에서는 현재 대출 중인 도서들의 목록을 볼 수 있어야 해.
각 대출 건에 대해 대출일, 반납예정일, 현재 상태(대출중/연체/반납완료)를 확인할 수 있어야 하고, 대출 중인 도서는 연장이나 반납 처리가 가능해야 해.
도서가 반납되면 자동으로 해당 도서의 상태가 '대출가능'으로 변경되어야 해.
만약 예약자가 있는 도서가 반납되면, 해당 도서는 '예약중' 상태로 변경되어야 해.

각 도서별로 대출 이력과 상태 변경 이력을 조회할 수 있어야 하고, 이를 통해 도서의 대출 현황과 상태 변화를 추적할 수 있어야 해.
"""))