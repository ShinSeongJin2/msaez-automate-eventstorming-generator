# client/simple_client.py
"""
비스트리밍 클라이언트 모듈
A2A 서버와 기본적인 요청/응답 통신을 합니다.
"""

import asyncio
import httpx
from a2a.client import A2AClient, A2ACardResolver, create_text_message_object
from a2a.types import (
    Role,
    MessageSendParams,
    SendMessageRequest,
)


# 서버 기본 URL
BASE_URL = "http://localhost:8000"


async def get_agent_info():
    """
    서버의 AgentCard 정보를 조회합니다.
    """
    print("\n" + "="*50)
    print("📇 AgentCard 조회 테스트")
    print("="*50)
    
    async with httpx.AsyncClient() as httpx_client:
        try:
            # A2ACardResolver를 사용하여 AgentCard 가져오기
            card_resolver = A2ACardResolver(
                httpx_client=httpx_client,
                base_url=BASE_URL,
            )
            agent_card = await card_resolver.get_agent_card()
            
            print(f"✅ 에이전트 이름: {agent_card.name}")
            print(f"✅ 설명: {agent_card.description}")
            print(f"✅ 버전: {agent_card.version}")
            print(f"✅ 스트리밍 지원: {agent_card.capabilities.streaming}")
            print(f"✅ 스킬 개수: {len(agent_card.skills)}")
            
            if agent_card.skills:
                print("\n📋 제공 스킬:")
                for skill in agent_card.skills:
                    print(f"  - {skill.name} ({skill.id}): {skill.description}")
            
            return agent_card
                
        except Exception as e:
            print(f"❌ 에러 발생: {str(e)}")
            print("💡 서버가 실행 중인지 확인하세요: python -m server.server")
            return None


async def send_greeting_request(name: str):
    """
    인사 요청을 보냅니다.
    
    Args:
        name: 사용자 이름
    """
    print("\n" + "="*50)
    print(f"💬 인사 요청 테스트: '{name}'")
    print("="*50)
    
    async with httpx.AsyncClient() as httpx_client:
        try:
            # 1. AgentCard 가져오기
            card_resolver = A2ACardResolver(
                httpx_client=httpx_client,
                base_url=BASE_URL,
            )
            agent_card = await card_resolver.get_agent_card()
            
            # 2. A2AClient 생성
            client = A2AClient(
                httpx_client=httpx_client,
                agent_card=agent_card,
            )
            
            # 3. 메시지 생성
            message = create_text_message_object(
                role=Role.user,
                content=name,
            )
            
            print(f"📤 요청 전송: {name}")
            
            # 4. SendMessageRequest 생성 및 전송
            request = SendMessageRequest(
                id="1",
                params=MessageSendParams(message=message),
            )
            
            response = await client.send_message(request)
            
            # 5. 결과 확인
            if hasattr(response, 'result') and response.result:
                task = response.result
                print(f"📥 Task ID: {task.id}")
                print(f"📊 상태: {task.status.state if task.status else 'N/A'}")
                
                # Artifact에서 결과 텍스트 추출
                if task.artifacts:
                    for artifact in task.artifacts:
                        if artifact.parts:
                            for part in artifact.parts:
                                if hasattr(part, 'text'):
                                    print(f"✅ 응답: {part.text}")
                else:
                    print("⚠️  응답 없음")
            else:
                print(f"⚠️  예상치 못한 응답: {response}")
                
        except Exception as e:
            print(f"❌ 에러 발생: {str(e)}")
            import traceback
            traceback.print_exc()
            print("💡 서버가 실행 중인지 확인하세요")


async def test_multiple_requests():
    """
    여러 요청을 연속으로 보내는 테스트
    """
    print("\n" + "="*50)
    print("🔄 연속 요청 테스트")
    print("="*50)
    
    async with httpx.AsyncClient() as httpx_client:
        # AgentCard 가져오기 (재사용)
        card_resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=BASE_URL,
        )
        agent_card = await card_resolver.get_agent_card()
        
        # A2AClient 생성
        client = A2AClient(
            httpx_client=httpx_client,
            agent_card=agent_card,
        )
        
        names = ["홍길동", "김철수", "이영희"]
        
        for idx, name in enumerate(names, start=1):
            try:
                # 메시지 생성
                message = create_text_message_object(
                    role=Role.user,
                    content=name,
                )
                
                print(f"\n📤 요청: {name}")
                
                # SendMessageRequest 생성 및 전송
                request = SendMessageRequest(
                    id=str(idx),
                    params=MessageSendParams(message=message),
                )
                
                response = await client.send_message(request)
                
                # 결과 확인
                if hasattr(response, 'result') and response.result:
                    task = response.result
                    if task.artifacts:
                        for artifact in task.artifacts:
                            if artifact.parts:
                                for part in artifact.parts:
                                    if hasattr(part, 'text'):
                                        print(f"✅ 응답: {part.text}")
                
                # 잠시 대기
                await asyncio.sleep(0.5)
                
            except Exception as e:
                print(f"❌ 에러: {str(e)}")


async def main():
    """
    메인 함수: 모든 테스트 실행
    """
    print("\n🚀 A2A 클라이언트 테스트 시작\n")
    
    # 테스트 1: AgentCard 조회
    await get_agent_info()
    
    # 테스트 2: 단일 요청
    await send_greeting_request("홍길동")
    
    # 테스트 3: 여러 요청
    await test_multiple_requests()
    
    print("\n" + "="*50)
    print("✅ 모든 테스트 완료!")
    print("="*50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
