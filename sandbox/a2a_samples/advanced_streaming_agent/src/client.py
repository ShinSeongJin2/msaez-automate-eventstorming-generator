import asyncio
from python_a2a import StreamingClient, Message, TextContent, MessageRole, A2AClient

"""
두 가지 호출 예:
1) StreamingClient로 토큰 스트리밍 수신
2) A2AClient.ask()로 간단 동기 호출
"""

async def stream_once():
    client = StreamingClient("http://localhost:5000")
    msg = Message(content=TextContent(text="스트리밍 테스트용 긴 문단을 요약해줘."), role=MessageRole.USER)

    print("=== streaming start ===")
    async for chunk in client.stream_response(msg):
        # chunk는 str 또는 dict일 수 있음 (라이브러리에서 다양한 청크 형식 지원)
        print(chunk if isinstance(chunk, str) else chunk.get("text") or chunk.get("content") or str(chunk), end="", flush=True)
    print("\n=== streaming end ===")

def simple_ask():
    client = A2AClient("http://localhost:5000")
    print("ASK:", client.ask("간단하게 이 문단을 요약해줘: ..."))

if __name__ == "__main__":
    asyncio.run(stream_once())
    simple_ask()