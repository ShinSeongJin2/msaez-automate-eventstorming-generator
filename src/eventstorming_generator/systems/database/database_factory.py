from typing import Dict

from .database_system import DatabaseSystem
from .firebase_system import FirebaseSystem
from .memory_db_system import MemoryDBSystem
from ...config import Config

class DatabaseFactory:
    _db_system_instance: Dict[str, DatabaseSystem] = {}

    @staticmethod
    def get_db_system() -> DatabaseSystem:
        """
        애플리케이션 환경에 맞는 DB 시스템 인스턴스를 반환합니다.
        싱글톤으로 동작하여 최초 호출 시 인스턴스를 생성하고 캐싱합니다.
        """
        db_type = Config.get_db_type()
        if db_type in DatabaseFactory._db_system_instance:
            return DatabaseFactory._db_system_instance[db_type]
        
        if db_type == "memory":
            DatabaseFactory._db_system_instance[db_type] = MemoryDBSystem()
        elif db_type == "firebase":
            DatabaseFactory._db_system_instance[db_type] = FirebaseSystem.initialize(
                service_account_path=Config.get_firebase_service_account_path(),
                database_url=Config.get_firebase_database_url()
            )
        else:
            raise Exception(f"Invalid database system type: {db_type}")
        
        return DatabaseFactory._db_system_instance[db_type]