import asyncio
import time
from typing import Optional

from ..systems import FirebaseSystem
from ..config import Config

class DecentralizedJobManager:
    def __init__(self, pod_id: str, job_processing_func: callable):
        self.pod_id = pod_id
        self.job_processing_func = job_processing_func
        self.current_job_id: Optional[str] = None  # 단일 Job 처리
        self.is_processing = False
        self.current_task: Optional[asyncio.Task] = None  # 현재 실행 중인 작업 태스크
    

    async def start_job_monitoring(self):
        """각 Pod가 독립적으로 작업 모니터링 - 순차 처리"""
        print(f"[{self.pod_id}] Job 모니터링 시작 (순차 처리 모드)")
        
        while True:
            try:
                print(f"[{self.pod_id}] Job 모니터링 중...")
                
                # 완료된 작업 확인 및 정리
                if self.current_task and self.current_task.done():
                    await self._handle_completed_task()
                
                if not self.is_processing:
                    # 현재 처리 중인 Job이 없을 때만 새 Job 검색
                    await self.find_and_process_next_job()
                
                # 현재 처리 중인 Job의 heartbeat 전송
                if self.current_job_id:
                    await self.send_heartbeat()
                
                # 실패한 작업 복구 (다른 Pod의 실패 작업)
                await self.recover_failed_jobs()
                
                await asyncio.sleep(15)  # 15초마다 체크
                
            except Exception as e:
                print(f"[{self.pod_id}] 작업 모니터링 오류: {e}")
                await asyncio.sleep(15)


    async def _handle_completed_task(self):
        """완료된 작업 태스크 처리"""
        if self.current_task:
            try:
                # 태스크에서 예외가 발생했는지 확인
                await self.current_task
            except Exception as e:
                print(f"[{self.pod_id}] Job {self.current_job_id} 처리 중 오류: {e}")
            finally:
                self.current_task = None


    async def find_and_process_next_job(self):
        """사용 가능한 다음 Job 찾기 및 처리 시작"""
        
        # 요청된 작업들 조회
        requested_jobs = await FirebaseSystem.instance().get_children_data_async(Config.get_requested_job_root_path())
        if not requested_jobs:
            return
        
        # 할당되지 않은 Job 찾기
        for job_id, job_data in requested_jobs.items():
            if job_data.get('assignedPodId') is None:
                success = await self.atomic_claim_job(job_id)
                if success:
                    # 성공적으로 클레임한 경우 해당 Job 처리 시작
                    await self.start_job_processing(job_id)
                    break  # 하나만 처리하고 종료
    
    async def atomic_claim_job(self, job_id: str) -> bool:
        """원자적 작업 클레임"""
        
        def update_function(current_data):
            if current_data is None:
                return None
            
            if current_data.get('assignedPodId') is None:
                current_data['assignedPodId'] = self.pod_id
                current_data['claimedAt'] = time.time()
                current_data['status'] = 'processing'
                current_data['lastHeartbeat'] = time.time()
                return current_data
            else:
                # 이미 할당됨
                return None
        
        try:
            ref = FirebaseSystem.instance().database.reference(Config.get_requested_job_path(job_id))
            result = await asyncio.get_event_loop().run_in_executor(
                None, lambda: ref.transaction(update_function)
            )
            
            if result is not None:
                print(f"[{self.pod_id}] 작업 {job_id} 클레임 성공")
                return True
            
        except Exception as e:
            print(f"[{self.pod_id}] 작업 클레임 실패: {e}")
        
        return False
    
    async def start_job_processing(self, job_id: str):
        """Job 처리 시작"""
        self.current_job_id = job_id
        self.is_processing = True
        
        print(f"[{self.pod_id}] Job {job_id} 처리 시작")
        
        # 실제 작업 수행
        await self.execute_job_logic(job_id)
    
    async def execute_job_logic(self, job_id: str):
        """실제 Job 로직 실행 - 비동기로 백그라운드에서 실행"""
        print(f"[{self.pod_id}] Job {job_id} 로직 실행 중...")
        
        # 작업을 백그라운드 태스크로 실행하여 heartbeat가 블록되지 않도록 함
        self.current_task = asyncio.create_task(
            self.job_processing_func(job_id, self.complete_job)
        )
    
    def complete_job(self):
        """Job 완료 처리"""
        print(f"[{self.pod_id}] Job {self.current_job_id} 처리 완료")

        self.current_job_id = None
        self.is_processing = False
        # current_task는 _handle_completed_task에서 정리됨

    async def send_heartbeat(self):
        """현재 처리 중인 Job의 heartbeat 전송"""
        if not self.current_job_id:
            return
        
        try:
            await FirebaseSystem.instance().update_data_async(
                Config.get_requested_job_path(self.current_job_id),
                {'lastHeartbeat': time.time()}
            )
        except Exception as e:
            print(f"[{self.pod_id}] Heartbeat 실패: {e}")
    

    async def recover_failed_jobs(self):
        """다른 Pod의 실패한 작업 복구"""
        try:
            current_time = time.time()
            requested_jobs = await FirebaseSystem.instance().get_children_data_async(Config.get_requested_job_root_path())
            
            if not requested_jobs:
                return
            
            for job_id, job_data in requested_jobs.items():
                assigned_pod = job_data.get('assignedPodId')
                last_heartbeat = job_data.get('lastHeartbeat', 0)
                
                # 다른 Pod가 할당했지만 5분간 heartbeat 없으면 실패로 간주
                if (assigned_pod and 
                    assigned_pod != self.pod_id and  # 다른 Pod의 Job만
                    current_time - last_heartbeat > 300 and
                    job_data.get('status') == 'processing'):
                    
                    print(f"[{self.pod_id}] 실패한 작업 감지: {job_id} (Pod: {assigned_pod})")
                    await self.reset_failed_job(job_id)
        
        except Exception as e:
            print(f"[{self.pod_id}] 실패 작업 복구 오류: {e}")
    
    async def reset_failed_job(self, job_id: str):
        """실패한 작업 초기화"""
        try:
            await FirebaseSystem.instance().update_data_async(
                Config.get_requested_job_path(job_id),
                {
                    'assignedPodId': None,
                    'status': 'pending',
                    'lastHeartbeat': None,
                }
            )
            print(f"[{self.pod_id}] 실패 작업 {job_id} 초기화 완료")
        except Exception as e:
            print(f"[{self.pod_id}] 실패 작업 초기화 오류: {e}")
    
    
    def get_status(self) -> dict:
        """현재 Pod 상태 반환"""
        return {
            'pod_id': self.pod_id,
            'is_processing': self.is_processing,
            'current_job_id': self.current_job_id,
            'status': 'processing' if self.is_processing else 'idle'
        }