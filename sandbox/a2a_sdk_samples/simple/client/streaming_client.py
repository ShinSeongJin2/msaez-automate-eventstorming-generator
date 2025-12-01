# client/streaming_client.py
"""
스트리밍 클라이언트 모듈
A2A 서버와 스트리밍 방식으로 통신합니다.
SSE(Server-Sent Events)를 통해 실시간으로 응답을 수신합니다.
"""

import asyncio
import httpx
from a2a.client import A2AClient, A2ACardResolver, create_text_message_object
from a2a.types import (
    Role,
    MessageSendParams,
    SendStreamingMessageRequest,
    TaskStatusUpdateEvent,
    TaskArtifactUpdateEvent,
    Task,
    Message,
)


# 서버 기본 URL
BASE_URL = "http://localhost:8000"


async def test_streaming_request(name: str = "홍길동"):
    """
    스트리밍 요청 테스트
    
    서버에 스트리밍 요청을 보내고, 실시간으로 응답 청크를 수신합니다.
    
    Args:
        name: 인사할 사용자 이름
    """
    print("\n" + "="*50)
    print(f"🌊 스트리밍 요청 테스트: '{name}'")
    print("="*50)
    
    async with httpx.AsyncClient(timeout=None) as httpx_client:
        try:
            # 1. AgentCard 가져오기
            card_resolver = A2ACardResolver(
                httpx_client=httpx_client,
                base_url=BASE_URL,
            )
            agent_card = await card_resolver.get_agent_card()
            
            print(f"📇 에이전트: {agent_card.name}")
            print(f"📡 스트리밍 지원: {agent_card.capabilities.streaming}")
            
            if not agent_card.capabilities.streaming:
                print("⚠️  이 에이전트는 스트리밍을 지원하지 않습니다!")
                return
            
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
            
            print(f"\n📤 스트리밍 요청 전송: {name}")
            print("-" * 40)
            
            # 4. SendStreamingMessageRequest 생성
            request = SendStreamingMessageRequest(
                id="streaming-1",
                params=MessageSendParams(message=message),
            )
            
            # 5. 스트리밍 응답 수신
            full_response = ""
            event_count = 0
            
            async for response in client.send_message_streaming(request):
                event_count += 1
                
                # response는 SendStreamingMessageResponse 타입
                # response.root가 실제 응답 객체 (SendStreamingMessageSuccessResponse)
                # response.root.result가 실제 이벤트 데이터
                actual_response = response.root if hasattr(response, 'root') else response
                result = actual_response.result if hasattr(actual_response, 'result') else None
                
                if result is None:
                    print(f"⚠️  result 없음: {response}")
                    continue
                    
                if isinstance(result, TaskStatusUpdateEvent):
                    # 상태 업데이트 이벤트
                    state = result.status.state if result.status else "unknown"
                    is_final = result.final
                    print(f"📊 상태: {state} (final: {is_final})")
                    
                elif isinstance(result, TaskArtifactUpdateEvent):
                    # Artifact 업데이트 이벤트 (실제 응답 데이터)
                    artifact = result.artifact
                    is_last_chunk = result.last_chunk
                    
                    if artifact and artifact.parts:
                        for part in artifact.parts:
                            # part는 Part 타입이고 part.root가 실제 TextPart
                            actual_part = part.root if hasattr(part, 'root') else part
                            if hasattr(actual_part, 'text'):
                                chunk_text = actual_part.text
                                full_response += chunk_text
                                # 실시간으로 청크 출력 (줄바꿈 없이)
                                print(chunk_text, end="", flush=True)
                    
                    if is_last_chunk:
                        print()  # 마지막 청크 후 줄바꿈
                        print(f"✅ 마지막 청크 수신")
                        
                elif isinstance(result, Task):
                    # 최종 Task 결과 (비스트리밍 응답 또는 최종 상태)
                    print(f"📋 Task ID: {result.id}")
                    print(f"📊 최종 상태: {result.status.state if result.status else 'N/A'}")
                    
                elif isinstance(result, Message):
                    # 메시지 응답
                    print(f"💬 메시지 수신")
                    if result.parts:
                        for part in result.parts:
                            actual_part = part.root if hasattr(part, 'root') else part
                            if hasattr(actual_part, 'text'):
                                print(f"   텍스트: {actual_part.text}")
                                
                else:
                    print(f"❓ 알 수 없는 응답 타입: {type(result)}")
            
            print("-" * 40)
            print(f"\n📈 통계:")
            print(f"   총 이벤트 수: {event_count}")
            print(f"   전체 응답: {full_response}")
            
        except Exception as e:
            print(f"❌ 에러 발생: {str(e)}")
            import traceback
            traceback.print_exc()
            print("💡 서버가 실행 중인지 확인하세요")


async def compare_streaming_vs_non_streaming(name: str = "김철수"):
    """
    스트리밍과 비스트리밍 요청 비교
    
    동일한 요청에 대해 두 가지 방식의 응답 시간과 결과를 비교합니다.
    
    Args:
        name: 인사할 사용자 이름
    """
    import time
    
    print("\n" + "="*50)
    print(f"📊 스트리밍 vs 비스트리밍 비교: '{name}'")
    print("="*50)
    
    async with httpx.AsyncClient(timeout=None) as httpx_client:
        try:
            # AgentCard 가져오기
            card_resolver = A2ACardResolver(
                httpx_client=httpx_client,
                base_url=BASE_URL,
            )
            agent_card = await card_resolver.get_agent_card()
            
            client = A2AClient(
                httpx_client=httpx_client,
                agent_card=agent_card,
            )
            
            message = create_text_message_object(
                role=Role.user,
                content=name,
            )
            
            # 비스트리밍 요청
            print("\n🔵 비스트리밍 요청:")
            print("-" * 30)
            start_time = time.time()
            
            from a2a.types import SendMessageRequest
            non_streaming_request = SendMessageRequest(
                id="non-streaming-1",
                params=MessageSendParams(message=message),
            )
            response = await client.send_message(non_streaming_request)
            
            non_streaming_time = time.time() - start_time
            
            if hasattr(response, 'result') and response.result:
                task = response.result
                if task.artifacts:
                    for artifact in task.artifacts:
                        if artifact.parts:
                            for part in artifact.parts:
                                if hasattr(part, 'text'):
                                    print(f"   응답: {part.text}")
            
            print(f"   소요 시간: {non_streaming_time:.2f}초")
            
            # 스트리밍 요청
            print("\n🟢 스트리밍 요청:")
            print("-" * 30)
            start_time = time.time()
            first_chunk_time = None
            
            streaming_request = SendStreamingMessageRequest(
                id="streaming-compare-1",
                params=MessageSendParams(message=message),
            )
            
            full_response = ""
            async for response in client.send_message_streaming(streaming_request):
                actual_response = response.root if hasattr(response, 'root') else response
                result = actual_response.result if hasattr(actual_response, 'result') else None
                
                if result and isinstance(result, TaskArtifactUpdateEvent):
                    if first_chunk_time is None:
                        first_chunk_time = time.time() - start_time
                    
                    if result.artifact and result.artifact.parts:
                        for part in result.artifact.parts:
                            actual_part = part.root if hasattr(part, 'root') else part
                            if hasattr(actual_part, 'text'):
                                full_response += actual_part.text
                                print(actual_part.text, end="", flush=True)
            
            streaming_time = time.time() - start_time
            print()  # 줄바꿈
            if first_chunk_time:
                print(f"   첫 청크 도착: {first_chunk_time:.2f}초")
            else:
                print(f"   첫 청크 도착: N/A")
            print(f"   총 소요 시간: {streaming_time:.2f}초")
            
            # 비교 결과
            print("\n📈 비교 결과:")
            print("-" * 30)
            print(f"   비스트리밍 총 시간: {non_streaming_time:.2f}초")
            if first_chunk_time:
                print(f"   스트리밍 첫 응답: {first_chunk_time:.2f}초")
            else:
                print(f"   스트리밍 첫 응답: N/A")
            print(f"   스트리밍 총 시간: {streaming_time:.2f}초")
            
            if first_chunk_time and first_chunk_time < non_streaming_time:
                improvement = ((non_streaming_time - first_chunk_time) / non_streaming_time) * 100
                print(f"   ✅ 첫 응답 속도 {improvement:.0f}% 개선!")
            
        except Exception as e:
            print(f"❌ 에러 발생: {str(e)}")
            import traceback
            traceback.print_exc()


async def main():
    """
    메인 함수: 스트리밍 테스트 실행
    """
    print("\n🚀 A2A 스트리밍 클라이언트 테스트 시작\n")
    
    # 테스트 1: 기본 스트리밍 요청
    await test_streaming_request("홍길동")
    
    # 테스트 2: 다른 이름으로 스트리밍 요청
    await test_streaming_request("이영희")
    
    # 테스트 3: 스트리밍 vs 비스트리밍 비교
    # await compare_streaming_vs_non_streaming("김철수")
    
    print("\n" + "="*50)
    print("✅ 모든 스트리밍 테스트 완료!")
    print("="*50 + "\n")


if __name__ == "__main__":
    asyncio.run(main())