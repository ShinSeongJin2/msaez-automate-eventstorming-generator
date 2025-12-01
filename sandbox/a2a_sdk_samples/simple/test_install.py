# test_install.py (수정 버전)
from a2a.types import AgentCard, AgentCapabilities, AgentSkill  # ✅ 정확한 임포트
import fastapi
import uvicorn

print("✅ a2a 임포트 성공!")
print(f"✅ FastAPI 버전: {fastapi.__version__}")
print("✅ 모든 패키지가 정상적으로 설치되었습니다!")

# 간단한 AgentCard 생성 테스트
card = AgentCard(
    name="테스트 에이전트",
    description="설치 테스트용 에이전트",
    url="http://localhost:9999",
    version="1.0.0",
    # 필수 필드들 추가
    capabilities=AgentCapabilities(),  # 기본 capabilities
    default_input_modes=["text"],       # 기본 입력 모드
    default_output_modes=["text"],      # 기본 출력 모드
    skills=[                            # 최소 하나의 skill 필요
        AgentSkill(
            id="test-skill",
            name="테스트 스킬",
            description="설치 테스트용 스킬",
            tags=["test"]
        )
    ]
)

print(f"✅ AgentCard 생성 성공: {card.name}")