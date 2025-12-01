# pizza_server.py
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from python_a2a import (
    A2AServer,
    agent,
    skill,
    run_server,
    TaskStatus,
    TaskState,
)

class PizzaState(TypedDict):
    messages: Annotated[list, add_messages]
    order: dict

def process_order(state: PizzaState):
    """피자 주문 처리 노드"""
    messages = state["messages"]
    last_msg = messages[-1].content if messages else ""
    
    # 간단한 주문 파싱
    order = {
        "size": "large" if "large" in last_msg.lower() else "medium",
        "toppings": [],
        "quantity": 1,
    }
    
    if "pepperoni" in last_msg.lower():
        order["toppings"].append("pepperoni")
    if "mushroom" in last_msg.lower():
        order["toppings"].append("mushroom")
    
    prices = {"small": 8.99, "medium": 12.99, "large": 15.99}
    total = prices[order["size"]] * order["quantity"]
    total += len(order["toppings"]) * 1.5
    
    order["total"] = total
    
    return {
        "order": order,
        "messages": [("assistant", f"주문 완료: {order['size']} 피자, 토핑: {order['toppings']}, 총액: ${total:.2f}")]
    }

@agent(
    name="Pizza Shop Agent",
    description="피자 주문을 처리하는 A2A 에이전트",
    version="1.0.0",
)
class PizzaAgent(A2AServer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # LangGraph 구성
        graph = StateGraph(PizzaState)
        graph.add_node("process_order", process_order)
        graph.add_edge(START, "process_order")
        graph.add_edge("process_order", END)
        self.graph = graph.compile()
    
    @skill(
        name="order_pizza",
        description="피자를 주문합니다",
        tags=["food", "pizza"],
    )
    def order_pizza(self, size: str, toppings: list, quantity: int = 1) -> dict:
        prices = {"small": 8.99, "medium": 12.99, "large": 15.99}
        total = prices.get(size, 12.99) * quantity
        total += len(toppings) * 1.5
        return {"size": size, "toppings": toppings, "quantity": quantity, "total": total}
    
    def handle_task(self, task):
        msg = task.message or {}
        content = msg.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else str(content)
        
        result = self.graph.invoke({
            "messages": [("user", text)],
            "order": {}
        })
        
        response = result["messages"][-1][1]
        
        task.artifacts = [{
            "parts": [{"type": "text", "text": response}]
        }]
        task.status = TaskStatus(state=TaskState.COMPLETED)
        
        return task

if __name__ == "__main__":
    pizza_agent = PizzaAgent(url="http://0.0.0.0:8003")
    run_server(pizza_agent, host="0.0.0.0", port=8003)