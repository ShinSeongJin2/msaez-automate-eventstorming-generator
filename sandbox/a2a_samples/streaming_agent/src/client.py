
"""
python_a2a 라이브러리를 사용한 스트리밍 클라이언트 예제
서버: StreamingAgent (port 5000)
"""
import asyncio
from python_a2a import StreamingClient, Message, TextContent, MessageRole

async def main():
    # A2AClient로 서버에 연결
    client = StreamingClient("http://localhost:5000")
    
    # 방법 1: 일반 요청 (비스트리밍)
    # print("=== Non-Streaming Request ===")
    # response = client.ask("Hello, this is a test message")
    # print(f"Response: {response}\n")
    
    # 방법 2: 스트리밍 요청
    print("=== Streaming Request ===")
    async for chunk in client.stream_response(
        Message(content=TextContent(text="This is a streaming test"), role=MessageRole.USER)
    ):
        # chunk는 보통 content 속성을 가짐
        if hasattr(chunk, 'content'):
            print(chunk.content, end="", flush=True)
        else:
            print(chunk, end="", flush=True)
    print("\n")

if __name__ == "__main__":
    asyncio.run(main())