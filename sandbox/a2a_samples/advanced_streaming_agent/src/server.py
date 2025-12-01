import os
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from python_a2a import run_server
from python_a2a.langchain import to_a2a_server

"""
사전 준비
- 환경변수 OPENAI_API_KEY 설정 필요.
- python_a2a 0.5.x 이상 권장.
"""

def build_server():
    # 간단한 요약 체인
    prompt = ChatPromptTemplate.from_template(
        "주어진 입력을 5문장 내로 간결히 요약하세요.\n입력:\n{input}\n\n요약:"
    )
    llm = ChatOpenAI(temperature=0)  # 모델은 필요에 맞게 지정
    chain = prompt | llm | StrOutputParser()

    # LangChain 컴포넌트를 A2A 서버로 변환
    # 내부적으로 A2A 규격에 맞춰 message/send, message/stream 등을 제공
    # `to_a2a_server(...)`로 LLM·체인을 바로 A2A 서버화할 수 있어 서버 구현 복잡도를 크게 줄입니다.
    server = to_a2a_server(chain)
    return server

if __name__ == "__main__":
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("환경변수 OPENAI_API_KEY를 설정하세요.")
    server = build_server()
    # 기본 0.0.0.0:5000
    run_server(server, host="0.0.0.0", port=5000)