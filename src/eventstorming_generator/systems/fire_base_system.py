import firebase_admin
from firebase_admin import credentials, db
from typing import Dict, Any, Optional

class FireBaseSystem:
    def __init__(self, service_account_path: str, database_url: str):
        """
        Firebase 시스템 초기화
        
        Args:
            service_account_path (str): Firebase 서비스 계정 JSON 키 파일 경로
            database_url (str): Firebase Realtime Database URL
        """
        try:
            # Firebase 앱이 이미 초기화되었는지 확인
            firebase_admin.get_app()
        except ValueError:
            # 앱이 초기화되지 않은 경우에만 초기화
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred, {
                'databaseURL': database_url
            })
        
        self.database = db
    
    def set_data(self, path: str, data: Dict[str, Any]) -> bool:
        """
        특정 경로에 딕셔너리 데이터를 업로드
        
        Args:
            path (str): Firebase 데이터베이스 경로 (예: 'users/user1')
            data (Dict[str, Any]): 업로드할 딕셔너리 데이터
            
        Returns:
            bool: 성공 여부
        """
        try:
            ref = self.database.reference(path)
            ref.set(data)
            return True
        except Exception as e:
            print(f"데이터 업로드 실패: {str(e)}")
            return False
    
    def get_data(self, path: str) -> Optional[Dict[str, Any]]:
        """
        특정 경로에서 데이터를 딕셔너리 형태로 조회
        
        Args:
            path (str): Firebase 데이터베이스 경로 (예: 'users/user1')
            
        Returns:
            Optional[Dict[str, Any]]: 조회된 데이터 (딕셔너리 형태) 또는 None
        """
        try:
            ref = self.database.reference(path)
            data = ref.get()
            
            if data is None:
                print(f"경로 '{path}'에 데이터가 없습니다.")
                return None
            
            return data
        except Exception as e:
            print(f"데이터 조회 실패: {str(e)}")
            return None
    
    def update_data(self, path: str, data: Dict[str, Any]) -> bool:
        """
        특정 경로의 데이터를 부분 업데이트
        
        Args:
            path (str): Firebase 데이터베이스 경로
            data (Dict[str, Any]): 업데이트할 딕셔너리 데이터
            
        Returns:
            bool: 성공 여부
        """
        try:
            ref = self.database.reference(path)
            ref.update(data)
            print(f"데이터가 성공적으로 업데이트되었습니다. 경로: {path}")
            return True
        except Exception as e:
            print(f"데이터 업데이트 실패: {str(e)}")
            return False

# Firebase 시스템 초기화
# firebase_system = FireBaseSystem(
#    service_account_path=os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH"),
#    database_url=os.getenv("FIREBASE_DATABASE_URL")
#)

# firebase_system.set_data(
#    "jobs/eventstorming_generator/1", 
#    {"state": {"isCompleted": False}}
#)

# print(firebase_system.get_data("jobs/eventstorming_generator/1"))

# firebase_system.update_data(
#    "jobs/eventstorming_generator/1",
#    {"state": {"isCompleted": True}}
#)