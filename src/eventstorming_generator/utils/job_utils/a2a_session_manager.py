import threading
from typing import Set


class A2ASessionManager:
    """
    A2A 스트리밍 세션을 관리하는 싱글톤 클래스
    
    활성 세션을 추적하여 Graceful Shutdown 시 
    모든 세션이 종료될 때까지 대기할 수 있도록 합니다.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._sessions: Set[str] = set()
                    cls._instance._session_lock = threading.Lock()
        return cls._instance
    
    @classmethod
    def instance(cls) -> 'A2ASessionManager':
        """싱글톤 인스턴스 반환"""
        return cls()
    
    def register_session(self, session_id: str) -> None:
        """새로운 A2A 스트리밍 세션 등록"""
        with self._session_lock:
            self._sessions.add(session_id)
    
    def unregister_session(self, session_id: str) -> None:
        """A2A 스트리밍 세션 해제"""
        with self._session_lock:
            self._sessions.discard(session_id)
    
    def has_active_sessions(self) -> bool:
        """활성 세션이 있는지 확인"""
        with self._session_lock:
            return len(self._sessions) > 0
    
    def get_active_session_count(self) -> int:
        """활성 세션 수 반환"""
        with self._session_lock:
            return len(self._sessions)
    
    def get_active_sessions(self) -> Set[str]:
        """활성 세션 ID 목록 반환 (복사본)"""
        with self._session_lock:
            return self._sessions.copy()

