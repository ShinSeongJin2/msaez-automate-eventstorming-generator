# server.py
import re
from python_a2a import (
    A2AServer,
    agent,
    skill,
    run_server,
    TaskStatus,
    TaskState,
)

@agent(
    name="Math Agent",
    description="두 정수를 더해 주는 A2A 에이전트",
    version="1.0.0",
)
class MathAgent(A2AServer):

    @skill(
        name="add",
        description="두 정수 a, b를 더합니다.",
        tags=["math", "add"],
    )
    def add(self, a: int, b: int) -> int:
        return a + b

    # A2A 요청을 받아 처리하는 최소 구현
    def handle_task(self, task):
        """
        task.message.content.text에 사용자가 보낸 텍스트가 들어옵니다.
        예) 'add 2 3', '2 + 3 더해줘' 등에서 숫자 2개를 추출해 덧셈.
        """
        msg = task.message or {}
        content = msg.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else str(content)

        # 텍스트에서 정수 2개 뽑기
        nums = list(map(int, re.findall(r"-?\d+", text)))
        if len(nums) >= 2:
            a, b = nums[0], nums[1]
            result = self.add(a, b)
            # A2A 규격에 맞춰 결과(artifact)를 적재하고 완료 상태로 세팅
            task.artifacts = [{
                "parts": [{"type": "text", "text": f"{a} + {b} = {result}"}]
            }]
            task.status = TaskStatus(state=TaskState.COMPLETED)
        else:
            # 입력 보강이 필요한 경우
            task.status = TaskStatus(
                state=TaskState.INPUT_REQUIRED,
                message={
                    "role": "agent",
                    "content": {"type": "text", "text": "예) 'add 2 3' 처럼 두 숫자를 보내주세요."}
                }
            )
        return task

if __name__ == "__main__":
    # 기본적으로 /.well-known/agent.json 로 Agent Card가 노출됩니다.
    # (A2A Python 서버 빌더는 해당 엔드포인트를 기본 제공) ([google-a2a.github.io](https://google-a2a.github.io/A2A/latest/tutorials/python/5-start-server/?utm_source=openai))
    math_agent = MathAgent(url="http://0.0.0.0:5000")
    run_server(math_agent, host="0.0.0.0", port=5000)  # 간단 실행 헬퍼 제공 ([github.com](https://github.com/themanojdesai/python-a2a))