import firebase_admin
from firebase_admin import credentials, db
from typing import Dict, Any, Optional
import os
import asyncio
import concurrent.futures
from functools import partial

class FirebaseSystem:
    _instance: Optional['FirebaseSystem'] = None
    _initialized: bool = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, service_account_path: str = None, database_url: str = None):
        """
        Firebase 시스템 초기화 (싱글톤)
        
        Args:
            service_account_path (str): Firebase 서비스 계정 JSON 키 파일 경로
            database_url (str): Firebase Realtime Database URL
        """
        # 이미 초기화된 경우 중복 초기화 방지
        if self._initialized:
            return
            
        if service_account_path is None or database_url is None:
            raise ValueError("service_account_path와 database_url은 필수 매개변수입니다.")
            
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
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self._initialized = True
    

    @classmethod
    def initialize(cls, service_account_path: str, database_url: str) -> 'FirebaseSystem':
        """
        싱글톤 인스턴스 초기화
        
        Args:
            service_account_path (str): Firebase 서비스 계정 JSON 키 파일 경로
            database_url (str): Firebase Realtime Database URL
            
        Returns:
            FirebaseSystem: 초기화된 싱글톤 인스턴스
        """
        if cls._instance is None or not cls._instance._initialized:
            cls._instance = cls(service_account_path, database_url)
        return cls._instance
    
    @classmethod
    def instance(cls) -> 'FirebaseSystem':
        """
        싱글톤 인스턴스 반환
        
        Returns:
            FirebaseSystem: 초기화된 싱글톤 인스턴스
            
        Raises:
            RuntimeError: 인스턴스가 초기화되지 않은 경우
        """
        if cls._instance is None or not cls._instance._initialized:
            raise RuntimeError("FirebaseSystem 초기화되지 않았습니다. 먼저 FirebaseSystem.initialize()를 호출하세요.")
        return cls._instance
    

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
    
    async def set_data_async(self, path: str, data: Dict[str, Any]) -> bool:
        """
        특정 경로에 딕셔너리 데이터를 비동기로 업로드
        
        Args:
            path (str): Firebase 데이터베이스 경로 (예: 'users/user1')
            data (Dict[str, Any]): 업로드할 딕셔너리 데이터
            
        Returns:
            bool: 성공 여부
        """
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(
                self._executor,
                partial(self._sync_set_data, path, data)
            )
            return result
        except Exception as e:
            print(f"비동기 데이터 업로드 실패: {str(e)}")
            return False
    
    def _sync_set_data(self, path: str, data: Dict[str, Any]) -> bool:
        """동기 set_data의 내부 구현"""
        try:
            ref = self.database.reference(path)
            ref.set(data)
            return True
        except Exception as e:
            print(f"데이터 업로드 실패: {str(e)}")
            return False
    
    def set_data_fire_and_forget(self, path: str, data: Dict[str, Any]) -> None:
        """
        Firebase에 데이터를 업로드하되 결과를 기다리지 않음 (Fire and Forget)
        
        Args:
            path (str): Firebase 데이터베이스 경로
            data (Dict[str, Any]): 업로드할 딕셔너리 데이터
        """
        try:
            # 새로운 이벤트 루프가 없는 경우를 대비한 처리
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # 이미 실행 중인 루프가 있으면 태스크로 추가
                    asyncio.create_task(self.set_data_async(path, data))
                else:
                    # 루프가 실행 중이 아니면 직접 실행
                    loop.run_until_complete(self.set_data_async(path, data))
            except RuntimeError:
                # 이벤트 루프가 없는 경우 새로 생성
                asyncio.run(self.set_data_async(path, data))
        except Exception as e:
            print(f"Fire and Forget 업로드 실패: {str(e)}")
    
    
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
            return True
        except Exception as e:
            print(f"데이터 업데이트 실패: {str(e)}")
            return False
    
    async def update_data_async(self, path: str, data: Dict[str, Any]) -> bool:
        """
        특정 경로의 데이터를 비동기로 부분 업데이트
        
        Args:
            path (str): Firebase 데이터베이스 경로
            data (Dict[str, Any]): 업데이트할 딕셔너리 데이터
            
        Returns:
            bool: 성공 여부
        """
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(
                self._executor,
                partial(self._sync_update_data, path, data)
            )
            return result
        except Exception as e:
            print(f"비동기 데이터 업데이트 실패: {str(e)}")
            return False
    
    def _sync_update_data(self, path: str, data: Dict[str, Any]) -> bool:
        """동기 update_data의 내부 구현"""
        try:
            ref = self.database.reference(path)
            ref.update(data)
            return True
        except Exception as e:
            print(f"데이터 업데이트 실패: {str(e)}")
            return False
    
    def update_data_fire_and_forget(self, path: str, data: Dict[str, Any]) -> None:
        """
        Firebase 데이터를 업데이트하되 결과를 기다리지 않음 (Fire and Forget)
        
        Args:
            path (str): Firebase 데이터베이스 경로
            data (Dict[str, Any]): 업데이트할 딕셔너리 데이터
        """
        try:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(self.update_data_async(path, data))
                else:
                    loop.run_until_complete(self.update_data_async(path, data))
            except RuntimeError:
                asyncio.run(self.update_data_async(path, data))
        except Exception as e:
            print(f"Fire and Forget 업데이트 실패: {str(e)}")


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
                return None
            
            return data
        except Exception as e:
            print(f"데이터 조회 실패: {str(e)}")
            return None

    def get_children_data(self, path: str) -> Optional[Dict[str, Dict[str, Any]]]:
        """
        특정 경로의 모든 자식 노드 데이터를 조회
        
        Args:
            path (str): Firebase 데이터베이스 경로 (예: 'jobs/eventstorming_generator')
            
        Returns:
            Optional[Dict[str, Dict[str, Any]]]: 자식 노드들의 데이터 (key: 자식 노드명, value: 데이터)
        """
        try:
            ref = self.database.reference(path)
            data = ref.get()
            
            if data is None or not isinstance(data, dict):
                return None
            
            return data
        except Exception as e:
            print(f"자식 데이터 조회 실패: {str(e)}")
            return None

    async def get_children_data_async(self, path: str) -> Optional[Dict[str, Dict[str, Any]]]:
        """
        특정 경로의 모든 자식 노드 데이터를 비동기로 조회
        
        Args:
            path (str): Firebase 데이터베이스 경로
            
        Returns:
            Optional[Dict[str, Dict[str, Any]]]: 자식 노드들의 데이터
        """
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(
                self._executor,
                partial(self._sync_get_children_data, path)
            )
            return result
        except Exception as e:
            print(f"비동기 자식 데이터 조회 실패: {str(e)}")
            return None

    def _sync_get_children_data(self, path: str) -> Optional[Dict[str, Dict[str, Any]]]:
        """동기 get_children_data의 내부 구현"""
        try:
            ref = self.database.reference(path)
            data = ref.get()
            
            if data is None or not isinstance(data, dict):
                return None
            
            return data
        except Exception as e:
            print(f"자식 데이터 조회 실패: {str(e)}")
            return None


    def delete_data(self, path: str) -> bool:
        """
        특정 경로의 데이터 삭제
        
        Args:
            path (str): Firebase 데이터베이스 경로
            
        Returns:
            bool: 성공 여부
        """
        try:
            ref = self.database.reference(path)
            ref.delete()
            return True
        except Exception as e:
            print(f"데이터 삭제 실패: {str(e)}")
            return False

    async def delete_data_async(self, path: str) -> bool:
        """
        특정 경로의 데이터를 비동기로 삭제
        
        Args:
            path (str): Firebase 데이터베이스 경로
            
        Returns:
            bool: 성공 여부
        """
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(
                self._executor,
                partial(self._sync_delete_data, path)
            )
            return result
        except Exception as e:
            print(f"비동기 데이터 삭제 실패: {str(e)}")
            return False
    
    def _sync_delete_data(self, path: str) -> bool:
        """동기 delete_data의 내부 구현"""
        try:
            ref = self.database.reference(path)
            ref.delete()
            return True
        except Exception as e:
            print(f"데이터 삭제 실패: {str(e)}")
            return False
    
    def delete_data_fire_and_forget(self, path: str) -> None:
        """
        Firebase 데이터를 삭제하되 결과를 기다리지 않음 (Fire and Forget)
        
        Args:
            path (str): Firebase 데이터베이스 경로
        """
        try:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(self.delete_data_async(path))
                else:
                    loop.run_until_complete(self.delete_data_async(path))
            except RuntimeError:
                asyncio.run(self.delete_data_async(path))
        except Exception as e:
            print(f"Fire and Forget 삭제 실패: {str(e)}")

FirebaseSystem.initialize(
    service_account_path=os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH"),
    database_url=os.getenv("FIREBASE_DATABASE_URL")
)