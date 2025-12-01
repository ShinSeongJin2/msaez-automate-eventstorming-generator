"""
A2A (Agent-to-Agent) 통신 모듈
EventStorming Generator의 A2A 프로토콜 구현을 제공합니다.
"""

from .agent_card import create_agent_card
from .agent_executor import EventStormingAgentExecutor

__all__ = [
    "create_agent_card",
    "EventStormingAgentExecutor",
]

