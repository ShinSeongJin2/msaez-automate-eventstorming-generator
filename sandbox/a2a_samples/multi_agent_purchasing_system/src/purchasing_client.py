# purchasing_client.py
from python_a2a import A2AClient

class PurchasingConcierge:
    """여러 A2A 에이전트를 조율하는 구매 대행 클라이언트"""
    
    def __init__(self):
        self.burger_client = A2AClient("http://localhost:8002")
        self.pizza_client = A2AClient("http://localhost:8003")
    
    def process_food_order(self, order_text: str):
        """주문 내용을 분석하여 적절한 에이전트로 라우팅"""
        order_text_lower = order_text.lower()
        
        results = []
        
        if any(word in order_text_lower for word in ["burger", "버거"]):
            print("🍔 Burger Agent에 주문 전송...")
            burger_response = self.burger_client.ask(order_text)
            results.append(("Burger Shop", burger_response))
        
        if any(word in order_text_lower for word in ["pizza", "피자"]):
            print("🍕 Pizza Agent에 주문 전송...")
            pizza_response = self.pizza_client.ask(order_text)
            results.append(("Pizza Shop", pizza_response))
        
        return results

def main():
    concierge = PurchasingConcierge()
    
    # 복합 주문 예시
    orders = [
        "I'd like 2 classic burgers and 1 large pepperoni pizza",
        "큰 치즈버거 3개 주문할게요",
        "medium pizza with mushroom topping please",
    ]
    
    for order in orders:
        print(f"\n📝 주문: {order}")
        print("-" * 60)
        
        results = concierge.process_food_order(order)
        
        for shop, response in results:
            print(f"\n[{shop}] 응답:")
            print(response)
        
        print("=" * 60)

if __name__ == "__main__":
    main()