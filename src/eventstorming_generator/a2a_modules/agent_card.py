"""
AgentCard 정의 모듈
EventStorming Generator 에이전트의 기본 정보와 스킬을 정의합니다.
"""

from a2a.types import (
    AgentCard,
    AgentCapabilities,
    AgentSkill
)


def create_agent_card(url: str = "http://localhost:5000") -> AgentCard:
    """
    EventStorming Generator 에이전트 카드를 생성합니다.
    
    Args:
        url: 에이전트 서버 URL
    
    Returns:
        AgentCard: 에이전트 정보
    """
    
    # 1. 에이전트가 제공할 스킬 정의
    event_storming_skill = AgentSkill(
        id="event_storming_generation",
        name="이벤트 스토밍 생성",
        description="요구사항을 기반으로 이벤트 스토밍 다이어그램을 자동 생성합니다",
        tags=["event-storming", "ddd", "domain-driven-design", "modeling"],
    )
    
    # 2. 에이전트의 기능(Capabilities) 정의 - 스트리밍만 지원
    capabilities = AgentCapabilities(
        streaming=True
    )
    
    # 3. AgentCard 생성
    card = AgentCard(
        name="EventStormingGeneratorAgent",
        description="이벤트 스토밍 생성 요청을 처리하는 A2A 에이전트입니다. 요구사항을 입력받아 도메인 주도 설계 기반의 이벤트 스토밍 다이어그램을 자동으로 생성합니다.",
        url=url,
        version="1.0.0",
        capabilities=capabilities,
        default_input_modes=["text"],
        default_output_modes=["text"],
        skills=[event_storming_skill],
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

