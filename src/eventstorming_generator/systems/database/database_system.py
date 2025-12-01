from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class DatabaseSystem(ABC):
    """
    데이터베이스 시스템을 위한 추상 기본 클래스입니다.
    데이터베이스 작업에 대한 공통 인터페이스를 정의합니다.
    """
    @abstractmethod
    def set_data(self, path: str, data: Dict[str, Any]) -> bool:
        """특정 경로에 데이터를 설정합니다."""
        pass

    @abstractmethod
    def get_data(self, path: str) -> Optional[Dict[str, Any]]:
        """특정 경로의 데이터를 가져옵니다."""
        pass

    @abstractmethod
    def update_data(self, path: str, data: Dict[str, Any]) -> bool:
        """특정 경로의 데이터를 업데이트합니다."""
        pass

    @abstractmethod
    def delete_data(self, path: str) -> bool:
        """특정 경로의 데이터를 삭제합니다."""
        pass

    @abstractmethod
    def conditional_update_data(self, path: str, data_to_update: Dict[str, Any], previous_data: Dict[str, Any]) -> bool:
        """
        두 데이터를 비교하여 변경된 부분만 효율적으로 업데이트합니다.
        
        Args:
            path (str): 데이터베이스 기본 경로
            data_to_update (Dict[str, Any]): 업데이트할 새로운 데이터
            previous_data (Dict[str, Any]): 기존 데이터
            
        Returns:
            bool: 성공 여부
        """
        pass


    def _find_data_differences(self, new_data: Dict[str, Any], old_data: Dict[str, Any], path_prefix: str = "") -> Dict[str, Any]:
        """
        두 딕셔너리를 재귀적으로 비교하여 차이점을 업데이트 형태로 반환
        
        Args:
            new_data (Dict[str, Any]): 새로운 데이터
            old_data (Dict[str, Any]): 기존 데이터
            path_prefix (str): 현재 경로 접두사
            
        Returns:
            Dict[str, Any]: 업데이트용 경로-값 딕셔너리
        """
        updates = {}
        
        # 새 데이터의 모든 키를 확인
        for key, new_value in new_data.items():
            current_path = f"{path_prefix}/{key}" if path_prefix else key
            old_value = old_data.get(key) if old_data else None
            
            # 값이 딕셔너리인 경우 재귀적으로 비교
            if isinstance(new_value, dict) and isinstance(old_value, dict):
                nested_updates = self._find_data_differences(new_value, old_value, current_path)
                updates.update(nested_updates)
            # 값이 다른 경우 업데이트 필요
            elif new_value != old_value:
                updates[current_path] = new_value
        
        # 기존 데이터에만 있고 새 데이터에 없는 키들은 삭제 처리
        if old_data:
            for key in old_data.keys():
                if key not in new_data:
                    current_path = f"{path_prefix}/{key}" if path_prefix else key
                    updates[current_path] = None  # 삭제를 위해 None 사용
        
        return updates