import re
import threading

from ..systems.firebase_system import FirebaseSystem
from ..models import State
from ..utils import JsonUtil

class JobUtil:
    @staticmethod
    def is_valid_job_id(job_id: str) -> bool:
        """
        JavaScript에서 생성된 UUID 형식의 JOB_ID 검증
        
        예상 형식: 8-4-4-4-12 (예: 5f8c86d1-16be-2ca9-0720-8a51f44439ab)
        
        Args:
            job_id (str): 검증할 JOB_ID
            
        Returns:
            bool: 유효한 JOB_ID 여부
        """
        if not job_id or not isinstance(job_id, str):
            return False
        
        # 1. 기본 길이 검증 (정확히 36자: 32개 16진수 + 4개 하이픈)
        if len(job_id) != 36:
            return False
        
        # 2. UUID 형식 검증 (8-4-4-4-12 패턴의 16진수)
        uuid_pattern = re.compile(
            r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$'
        )
        
        if not uuid_pattern.match(job_id):
            return False
        
        # 3. 하이픈 위치 정확성 검증
        expected_hyphen_positions = [8, 13, 18, 23]
        for pos in expected_hyphen_positions:
            if job_id[pos] != '-':
                return False
        
        # 4. 16진수 부분만 추출하여 추가 검증
        hex_parts = job_id.split('-')
        expected_lengths = [8, 4, 4, 4, 12]
        
        if len(hex_parts) != 5:
            return False
            
        for i, part in enumerate(hex_parts):
            if len(part) != expected_lengths[i]:
                return False
            # 각 부분이 유효한 16진수인지 확인
            try:
                int(part, 16)
            except ValueError:
                return False
        
        # 5. 보안 검증: 경로 조작 문자 금지
        forbidden_chars = ['/', '\\', '..', '#', '$', '[', ']', '?', '&']
        if any(char in job_id for char in forbidden_chars):
            return False
        
        return True


    @staticmethod
    def new_job_to_firebase(state: State):
        FirebaseSystem.instance().set_data(
            f"jobs/eventstorming_generator/{state.inputs.jobId}",
            {
                "state": JsonUtil.convert_to_json(state)
            }
        )

    @staticmethod
    async def new_job_to_firebase_async(state: State) -> bool:
        """
        새로운 작업을 Firebase에 비동기로 업로드
        
        Args:
            state (State): 업로드할 상태 객체
            
        Returns:
            bool: 성공 여부
        """
        return await FirebaseSystem.instance().set_data_async(
            f"jobs/eventstorming_generator/{state.inputs.jobId}",
            {
                "state": JsonUtil.convert_to_json(state)
            }
        )
    
    @staticmethod
    def new_job_to_firebase_fire_and_forget(state: State):
        """
        새로운 작업을 Firebase에 업로드하되 결과를 기다리지 않음
        백그라운드에서 실행되어 메인 코드 실행을 차단하지 않음
        
        Args:
            state (State): 업로드할 상태 객체
        """
        def _async_wrapper():
            try:
                FirebaseSystem.instance().set_data_fire_and_forget(
                    f"jobs/eventstorming_generator/{state.inputs.jobId}",
                    {
                        "state": JsonUtil.convert_to_json(state)
                    }
                )
            except Exception as e:
                print(f"백그라운드 Firebase 업로드 실패: {str(e)}")
        
        # 별도 스레드에서 실행하여 메인 스레드를 차단하지 않음
        thread = threading.Thread(target=_async_wrapper, daemon=True)
        thread.start()


    @staticmethod
    def update_job_to_firebase(state: State):
        FirebaseSystem.instance().update_data(
            f"jobs/eventstorming_generator/{state.inputs.jobId}",
            {
                "state": JsonUtil.convert_to_json(state)
            }
        )

    @staticmethod
    async def update_job_to_firebase_async(state: State) -> bool:
        """
        작업 상태를 Firebase에 비동기로 업데이트
        
        Args:
            state (State): 업데이트할 상태 객체
            
        Returns:
            bool: 성공 여부
        """
        return await FirebaseSystem.instance().update_data_async(
            f"jobs/eventstorming_generator/{state.inputs.jobId}",
            {
                "state": JsonUtil.convert_to_json(state)
            }
        )
    
    @staticmethod
    def update_job_to_firebase_fire_and_forget(state: State):
        """
        작업 상태를 Firebase에 업데이트하되 결과를 기다리지 않음
        백그라운드에서 실행되어 메인 코드 실행을 차단하지 않음
        
        Args:
            state (State): 업데이트할 상태 객체
        """
        def _async_wrapper():
            try:
                FirebaseSystem.instance().update_data_fire_and_forget(
                    f"jobs/eventstorming_generator/{state.inputs.jobId}",
                    {
                        "state": JsonUtil.convert_to_json(state)
                    }
                )
            except Exception as e:
                print(f"백그라운드 Firebase 업데이트 실패: {str(e)}")
        
        # 별도 스레드에서 실행하여 메인 스레드를 차단하지 않음
        thread = threading.Thread(target=_async_wrapper, daemon=True)
        thread.start()