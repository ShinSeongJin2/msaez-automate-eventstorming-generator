# client.py
from python_a2a import A2AClient

def main():
    # Currency Agent에 연결
    client = A2AClient("http://localhost:5000")
    
    # LangGraph를 통한 일반적인 질의
    queries = [
        "100 USD를 KRW로 환전하면 얼마인가요?",
        "EUR과 USD의 환율은?",
        "50000 JPY를 USD로 바꿔주세요",
    ]
    
    for query in queries:
        print(f"\n질문: {query}")
        response = client.ask(query)
        print(f"응답: {response}")

if __name__ == "__main__":
    main()