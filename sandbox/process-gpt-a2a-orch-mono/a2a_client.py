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
    asyncio.run(send_message_to_agent("http://localhost:8000", "Hello, how are you?"))