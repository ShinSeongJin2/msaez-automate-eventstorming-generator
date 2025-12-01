# client.py
from python_a2a import A2AClient

if __name__ == "__main__":
    # 서버의 베이스 URL을 전달
    client = A2AClient("http://localhost:5000")

    # 가장 간단한 질의 편의 메서드: ask()
    # 내부적으로 A2A message/send 요청을 만들어 전송하고,
    # 응답 텍스트(artifact)를 편의 형태로 반환합니다. ([github.com](https://github.com/themanojdesai/python-a2a))
    print(client.ask("add 2 3"))         # -> "2 + 3 = 5"
    print(client.ask("100과 -7을 더해줘"))  # -> "100 + -7 = 93"