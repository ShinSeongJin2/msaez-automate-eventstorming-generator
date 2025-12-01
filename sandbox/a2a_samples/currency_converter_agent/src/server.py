# server.py
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from python_a2a import (
    A2AServer,
    agent,
    skill,
    run_server,
    TaskStatus,
    TaskState,
)
import os

# LangGraph State 정의
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 환율 조회 도구
def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """실제로는 API 호출, 여기서는 간단히 하드코딩"""
    rates = {
        ("USD", "KRW"): 1320.5,
        ("EUR", "USD"): 1.08,
        ("GBP", "USD"): 1.27,
        ("JPY", "USD"): 0.0067,
    }
    return rates.get((from_currency.upper(), to_currency.upper()), 1.0)

def convert_currency(amount: float, from_currency: str, to_currency: str) -> dict:
    """환전 계산"""
    rate = get_exchange_rate(from_currency, to_currency)
    converted = amount * rate
    return {
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
        "rate": rate,
        "result": converted
    }

# LangGraph 그래프 구성
def build_currency_graph():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    # 도구를 LLM에 바인딩
    tools = [convert_currency, get_exchange_rate]
    llm_with_tools = llm.bind_tools(tools)
    
    def chatbot(state: State):
        return {"messages": [llm_with_tools.invoke(state["messages"])]}
    
    graph = StateGraph(State)
    graph.add_node("chatbot", chatbot)
    graph.add_edge(START, "chatbot")
    graph.add_edge("chatbot", END)
    
    return graph.compile()

@agent(
    name="Currency Converter Agent",
    description="환율 조회 및 환전 계산을 수행하는 A2A 에이전트",
    version="1.0.0",
)
class CurrencyAgent(A2AServer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.graph = build_currency_graph()
    
    @skill(
        name="convert_currency",
        description="금액을 한 통화에서 다른 통화로 환전합니다",
        tags=["currency", "conversion"],
    )
    def convert(self, amount: float, from_currency: str, to_currency: str) -> dict:
        return convert_currency(amount, from_currency, to_currency)
    
    @skill(
        name="get_exchange_rate",
        description="두 통화 간 환율을 조회합니다",
        tags=["currency", "rate"],
    )
    def get_rate(self, from_currency: str, to_currency: str) -> float:
        return get_exchange_rate(from_currency, to_currency)
    
    def handle_task(self, task):
        """LangGraph를 사용한 A2A 태스크 처리"""
        msg = task.message or {}
        content = msg.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else str(content)
        
        try:
            # LangGraph 그래프 실행
            result = self.graph.invoke({
                "messages": [("user", text)]
            })
            
            # 응답 추출
            last_message = result["messages"][-1]
            response_text = last_message.content
            
            # A2A 규격으로 결과 반환
            task.artifacts = [{
                "parts": [{"type": "text", "text": response_text}]
            }]
            task.status = TaskStatus(state=TaskState.COMPLETED)
            
        except Exception as e:
            task.status = TaskStatus(
                state=TaskState.FAILED,
                message={
                    "role": "agent",
                    "content": {"type": "text", "text": f"Error: {str(e)}"}
                }
            )
        
        return task

if __name__ == "__main__":
    currency_agent = CurrencyAgent(url="http://0.0.0.0:5000")
    run_server(currency_agent, host="0.0.0.0", port=5000)