from python_a2a import A2AClient

if __name__ == "__main__":
    client = A2AClient("http://localhost:6000")

    # 사람이 읽을 텍스트
    print(client.ask("paris 3 days plan"))
    # JSON이 함께 들어오므로 필요하면 직접 Task를 받아 파싱하는 메서드로 확장 가능
    # (라이브러리의 고급 클라이언트/네트워크 기능은 아래 문서들을 참고)
    # - StreamingClient, AgentNetwork, Discovery, CLI/UI 등