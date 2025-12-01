"""
A2A 서버 실행 모듈
FastAPI 기반 A2A 서버를 시작합니다.
헬스체크 엔드포인트도 포함됩니다.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from a2a.server.apps.jsonrpc.fastapi_app import A2AFastAPIApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.server.events import InMemoryQueueManager

from eventstorming_generator.a2a_modules import create_agent_card, EventStormingAgentExecutor
from eventstorming_generator.utils.logging_util import LoggingUtil
from eventstorming_generator.config import Config


def create_app(host: str = "0.0.0.0", port: int = 5000) -> FastAPI:
    """
    FastAPI 애플리케이션을 생성합니다.
    
    Args:
        host: 서버 호스트
        port: 서버 포트
    
    Returns:
        FastAPI: FastAPI 앱 인스턴스
    """
    
    # 1. AgentCard 생성
    agent_card = create_agent_card(url=f"http://{host}:{port}")
    LoggingUtil.info("run_a2a_server", f"AgentCard 생성: {agent_card.name}")
    
    # 2. AgentExecutor 생성
    agent_executor = EventStormingAgentExecutor()
    LoggingUtil.info("run_a2a_server", f"AgentExecutor 생성: {agent_executor.__class__.__name__}")
    
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
    
    # 7. CORS 설정
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    LoggingUtil.info("run_a2a_server", "A2A 서버 설정 완료!")
    
    # 8. 헬스체크 엔드포인트 (/ok)
    @app.get("/ok")
    async def health_check():
        """헬스체크 엔드포인트"""
        return {
            "status": "ok",
            "message": "EventStorming Generator 서버가 정상 작동 중입니다."
        }
    
    # 9. 루트 엔드포인트 (서버 상태 확인용)
    @app.get("/")
    async def root():
        return {
            "message": "EventStorming Generator A2A Server is running!",
            "agent": agent_card.name,
            "version": agent_card.version,
            "endpoints": {
                "agent_card": "/.well-known/agent.json",
                "health_check": "/ok",
                "rpc": "/",
            }
        }
    
    return app


def run_a2a_server(host: str = "0.0.0.0", port: int = 5000):
    """
    A2A 서버를 실행합니다.
    별도 스레드에서 호출되어 동기적으로 실행됩니다.
    
    Args:
        host: 서버 호스트 (기본: localhost)
        port: 서버 포트 (기본: 5000)
    """
    # 로컬 환경 > localhost, k8s 환경 > 0.0.0.0
    if Config.is_local_run():
        host = "localhost"

    app = create_app(host, port)
    
    LoggingUtil.info("run_a2a_server", f"A2A 서버 시작: http://{host}:{port}")
    LoggingUtil.info("run_a2a_server", f"Agent Card: http://{host}:{port}/.well-known/agent.json")
    LoggingUtil.info("run_a2a_server", f"헬스체크: http://{host}:{port}/ok")
    
    # uvicorn 로그 레벨 설정 (헬스체크 로그 최소화)
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="warning",
    )


if __name__ == "__main__":
    run_a2a_server()
