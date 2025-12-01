# burger_server.py
from crewai import Agent, Task, Crew
from python_a2a import (
    A2AServer,
    agent,
    skill,
    run_server,
    TaskStatus,
    TaskState,
)

@agent(
    name="Burger Shop Agent",
    description="버거 주문을 처리하는 A2A 에이전트",
    version="1.0.0",
)
class BurgerAgent(A2AServer):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # CrewAI Agent 정의
        self.sales_agent = Agent(
            role="Burger Sales Representative",
            goal="고객의 버거 주문을 받고 가격을 계산합니다",
            backstory="당신은 친절한 버거 가게 직원입니다",
            allow_delegation=False,
        )
    
    @skill(
        name="order_burger",
        description="버거를 주문하고 총 가격을 계산합니다",
        tags=["food", "order"],
    )
    def order_burger(self, burger_type: str, quantity: int) -> dict:
        prices = {
            "classic": 5.99,
            "cheese": 6.99,
            "bacon": 7.99,
            "deluxe": 9.99,
        }
        price = prices.get(burger_type.lower(), 5.99)
        total = price * quantity
        
        return {
            "burger": burger_type,
            "quantity": quantity,
            "unit_price": price,
            "total": total,
            "status": "confirmed"
        }
    
    def handle_task(self, task):
        msg = task.message or {}
        content = msg.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else str(content)
        
        # CrewAI Task 생성
        order_task = Task(
            description=f"Process this burger order: {text}",
            expected_output="Order confirmation with total price",
            agent=self.sales_agent,
        )
        
        crew = Crew(
            agents=[self.sales_agent],
            tasks=[order_task],
        )
        
        try:
            result = crew.kickoff()
            
            task.artifacts = [{
                "parts": [{"type": "text", "text": str(result)}]
            }]
            task.status = TaskStatus(state=TaskState.COMPLETED)
        except Exception as e:
            task.status = TaskStatus(
                state=TaskState.FAILED,
                message={"role": "agent", "content": {"type": "text", "text": str(e)}}
            )
        
        return task

if __name__ == "__main__":
    burger_agent = BurgerAgent(url="http://0.0.0.0:8002")
    run_server(burger_agent, host="0.0.0.0", port=8002)