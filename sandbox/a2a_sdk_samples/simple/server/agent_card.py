# server/agent_card.py
"""
AgentCard 정의 모듈
에이전트의 기본 정보와 스킬을 정의합니다.
"""

from a2a.types import (
    AgentCard,
    AgentCapabilities,
    AgentSkill
)


def create_agent_card() -> AgentCard:
    """
    인사 에이전트 카드를 생성합니다.
    
    Returns:
        AgentCard: 에이전트 정보
    """
    
    # 1. 에이전트가 제공할 스킬 정의
    greeting_skill = AgentSkill(
        id="greeting",
        name="인사하기",
        description="사용자에게 친근한 인사를 합니다",
        tags=["greeting", "hello"],
    )
    
    # 2. 에이전트의 기능(Capabilities) 정의
    capabilities = AgentCapabilities(
        streaming=True
    )
    
    # 3. AgentCard 생성
    card = AgentCard(
        name="인사 에이전트",
        description="사용자에게 따뜻한 인사를 전하는 에이전트입니다",
        url="http://localhost:8000",  # 서버 주소
        version="1.0.0",
        capabilities=capabilities,
        default_input_modes=["text"],   # 텍스트 입력
        default_output_modes=["text"], # 텍스트 출력
        skills=[greeting_skill],
    )
    
    return card


if __name__ == "__main__":
    # 테스트: AgentCard 생성 및 출력
    card = create_agent_card()
    print("✅ AgentCard 생성 성공!")
    print(f"📝 이름: {card.name}")
    print(f"📝 설명: {card.description}")
    print(f"📝 스킬 개수: {len(card.skills)}")
    print(f"📝 스트리밍 지원: {card.capabilities.streaming}")