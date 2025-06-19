import asyncio
import time
from typing import Optional, List, Tuple

from ..systems import FirebaseSystem
from ..config import Config
from .logging_util import LoggingUtil

class DecentralizedJobManager:
    def __init__(self, pod_id: str, job_processing_func: callable):
        self.pod_id = pod_id
        self.job_processing_func = job_processing_func
        self.current_job_id: Optional[str] = None  # 단일 Job 처리
        self.is_processing = False
        self.current_task: Optional[asyncio.Task] = None  # 현재 실행 중인 작업 태스크
    

    async def start_job_monitoring(self):
        """각 Pod가 독립적으로 작업 모니터링 - 순차 처리"""
        LoggingUtil.info("decentralized_job_manager", f"Job 모니터링 시작 (순차 처리 모드)")
        
        while True:
            try:
                LoggingUtil.debug("decentralized_job_manager", f"Job 모니터링 중...")

                requested_jobs = await FirebaseSystem.instance().get_children_data_async(Config.get_requested_job_root_path())
                
                # 완료된 작업 확인 및 정리
                if self.current_task and self.current_task.done():
                    await self._handle_completed_task()
                
                if not self.is_processing:
                    # 현재 처리 중인 Job이 없을 때만 새 Job 검색
                    await self.find_and_process_next_job(requested_jobs)
                
                # 현재 처리 중인 Job의 heartbeat 전송
                if self.current_job_id:
                    await self.send_heartbeat()
                
                # 대기 중인 작업들의 waitingJobCount 업데이트
                await self.update_waiting_job_counts(requested_jobs)
                
                # 실패한 작업 복구 (다른 Pod의 실패 작업)
                await self.recover_failed_jobs(requested_jobs)
                
                await asyncio.sleep(15)  # 15초마다 체크
                
            except Exception as e:
                LoggingUtil.exception("decentralized_job_manager", f"작업 모니터링 오류", e)
                await asyncio.sleep(15)


    async def _handle_completed_task(self):
        """완료된 작업 태스크 처리"""
        if self.current_task:
            try:
                # 태스크에서 예외가 발생했는지 확인
                await self.current_task
            except Exception as e:
                LoggingUtil.exception("decentralized_job_manager", f"Job {self.current_job_id} 처리 중 오류", e)
            finally:
                self.current_task = None


    async def find_and_process_next_job(self, requested_jobs: dict):
        """사용 가능한 다음 Job 찾기 및 처리 시작 (FIFO 순서)"""
        
        if not requested_jobs:
            return
        
        # createdAt 기준으로 정렬 (FIFO)
        sorted_jobs = self._sort_jobs_by_created_at(requested_jobs)
        
        # 할당되지 않은 Job 찾기 (시간순으로)
        for job_id, job_data in sorted_jobs:
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
            
            current_data = FirebaseSystem.instance().restore_data_from_firebase(current_data)
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
                LoggingUtil.debug("decentralized_job_manager", f"작업 {job_id} 클레임 성공")
                return True
            
        except Exception as e:
            LoggingUtil.exception("decentralized_job_manager", f"작업 클레임 실패", e)
        
        return False
    
    async def start_job_processing(self, job_id: str):
        """Job 처리 시작"""
        self.current_job_id = job_id
        self.is_processing = True
        
        LoggingUtil.debug("decentralized_job_manager", f"Job {job_id} 처리 시작")
        
        # 실제 작업 수행
        await self.execute_job_logic(job_id)
    
    async def execute_job_logic(self, job_id: str):
        """실제 Job 로직 실행 - 비동기로 백그라운드에서 실행"""
        LoggingUtil.debug("decentralized_job_manager", f"Job {job_id} 로직 실행 중...")
        
        # 작업을 백그라운드 태스크로 실행하여 heartbeat가 블록되지 않도록 함
        self.current_task = asyncio.create_task(
            self.job_processing_func(job_id, self.complete_job)
        )

    def complete_job(self):
        """Job 완료 처리"""
        LoggingUtil.debug("decentralized_job_manager", f"Job {self.current_job_id} 처리 완료")

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
            LoggingUtil.exception("decentralized_job_manager", f"Heartbeat 실패", e)
    

    async def update_waiting_job_counts(self, requested_jobs: dict):
        """대기 중인 작업들의 waitingJobCount 업데이트"""
        try:
            if not requested_jobs:
                return
            
            # createdAt 기준으로 정렬
            sorted_jobs = self._sort_jobs_by_created_at(requested_jobs)
            
            # 대기 중인 작업들만 필터링 (assignedPodId가 없는 것들)
            waiting_jobs = []
            for job_id, job_data in sorted_jobs:
                if job_data.get('assignedPodId') is None:
                    waiting_jobs.append((job_id, job_data))
            
            # 각 대기 중인 작업의 waitingJobCount 계산 및 업데이트
            for index, (job_id, job_data) in enumerate(waiting_jobs):
                waiting_count = index + 1  # 앞에 있는 대기 작업의 개수(대기중인 상태이기 때문에 기본적으로 1개 추가)
                current_waiting_count = job_data.get('waitingJobCount')
                
                # waitingJobCount가 없거나 기존 값과 다를 경우에만 업데이트
                if current_waiting_count != waiting_count:
                    await FirebaseSystem.instance().update_data_async(
                        Config.get_requested_job_path(job_id),
                        {'waitingJobCount': waiting_count}
                    )
                    LoggingUtil.debug("decentralized_job_manager", f"Job {job_id} waitingJobCount 업데이트: {waiting_count}")
                    
        except Exception as e:
            LoggingUtil.exception("decentralized_job_manager", f"waitingJobCount 업데이트 오류", e)
    

    async def recover_failed_jobs(self, requested_jobs: dict):
        """다른 Pod의 실패한 작업 복구"""
        try:     
            if not requested_jobs:
                return
            
            current_time = time.time()
            for job_id, job_data in requested_jobs.items():
                assigned_pod = job_data.get('assignedPodId')
                last_heartbeat = job_data.get('lastHeartbeat', 0)
                
                # 다른 Pod가 할당했지만 5분간 heartbeat 없으면 실패로 간주
                if (assigned_pod and 
                    current_time - last_heartbeat > 300 and
                    job_data.get('status') == 'processing'):
                    
                    LoggingUtil.warning("decentralized_job_manager", f"실패한 작업 감지: {job_id} (Pod: {assigned_pod})")
                    await self.reset_failed_job(job_id)
        except Exception as e:
            LoggingUtil.exception("decentralized_job_manager", f"실패 작업 복구 오류", e)
    
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
            LoggingUtil.debug("decentralized_job_manager", f"실패 작업 {job_id} 초기화 완료")
        except Exception as e:
            LoggingUtil.exception("decentralized_job_manager", f"실패 작업 초기화 오류", e)
    
    
    def _sort_jobs_by_created_at(self, jobs_dict: dict) -> List[Tuple[str, dict]]:
        """createdAt 기준으로 작업들을 시간순(FIFO)으로 정렬"""
        jobs_list = [(job_id, job_data) for job_id, job_data in jobs_dict.items()]
        
        # createdAt 기준으로 정렬 (오래된 것부터)
        jobs_list.sort(key=lambda x: x[1].get('createdAt', 0))
        
        return jobs_list