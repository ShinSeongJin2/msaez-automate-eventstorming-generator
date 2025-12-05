# server/server_for_process_gpt.py
"""
FastAPI 서버 실행 모듈 (Process GPT용)
a2a_client.py와 호환되는 A2A 서버를 시작합니다.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from a2a.server.apps.jsonrpc.fastapi_app import A2AFastAPIApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.events import InMemoryQueueManager

from server.agent_card import create_agent_card
from server.agent_executor_for_process_gpt import GreetingAgentExecutorForProcessGPT


def create_app() -> FastAPI:
    """
    FastAPI 애플리케이션을 생성합니다.
    
    Returns:
        FastAPI: FastAPI 앱 인스턴스
    """
    
    # 1. AgentCard 생성
    agent_card = create_agent_card()
    print(f"📇 AgentCard 생성: {agent_card.name}")
    
    # 2. AgentExecutor 생성 (Process GPT용)
    agent_executor = GreetingAgentExecutorForProcessGPT()
    print(f"⚙️  AgentExecutor 생성: {agent_executor.__class__.__name__}")
    
    # 3. TaskStore, QueueManager 생성 (메모리 기반)
    task_store = InMemoryTaskStore()
    queue_manager = InMemoryQueueManager()
    
    # 4. RequestHandler 생성
    request_handler = DefaultRequestHandler(
        agent_executor=agent_executor,
        task_store=task_store,
        queue_manager=queue_manager,
    )
    
    # 5. A2A FastAPI 애플리케이션 생성
    a2a_app = A2AFastAPIApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )
    
    # 6. FastAPI 앱 가져오기
    app = a2a_app.build()
    
    # 7. CORS 설정 (클라이언트가 다른 도메인에서 접근 가능하도록)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # 실제 프로덕션에서는 특정 도메인만 허용
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    print("✅ A2A 서버 설정 완료! (Process GPT용)")
    
    # 8. 루트 엔드포인트 추가 (서버 상태 확인용)
    @app.get("/")
    async def root():
        return {
            "message": "A2A Greeting Agent Server is running! (Process GPT Edition)",
            "agent": agent_card.name,
            "version": agent_card.version,
            "executor": "GreetingAgentExecutorForProcessGPT",
            "endpoints": {
                "agent_card": "/.well-known/agent.json",
                "rpc": "/",
            }
        }
    
    # 9. 헬스 체크 엔드포인트
    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "executor": "GreetingAgentExecutorForProcessGPT"}
    
    return app


def run_server(host: str = "0.0.0.0", port: int = 8000):
    """
    서버를 실행합니다.
    
    Args:
        host: 서버 호스트 (기본: 0.0.0.0 - 모든 네트워크 인터페이스)
        port: 서버 포트 (기본: 8000)
    """
    app = create_app()
    
    print("\n" + "="*50)
    print(f"🚀 A2A 서버 시작! (Process GPT용)")
    print(f"📍 주소: http://{host}:{port}")
    print(f"📖 API 문서: http://{host}:{port}/docs")
    print(f"📇 Agent Card: http://{host}:{port}/.well-known/agent.json")
    print(f"🔧 Executor: GreetingAgentExecutorForProcessGPT")
    print("="*50 + "\n")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
    )


if __name__ == "__main__":
    # 개발 서버 실행
    run_server()

