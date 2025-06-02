import re
import threading
from typing import Callable
import asyncio
import queue
import time
from dataclasses import dataclass
from typing import Dict, Optional
import atexit
import weakref

from ..systems.firebase_system import FirebaseSystem
from ..models import State
from ..utils import JsonUtil

@dataclass
class UpdateRequest:
    """Firebase 업데이트 요청 데이터 클래스"""
    state: State
    timestamp: float
    operation_type: str  # 'update', 'set', 'delete'
    path_suffix: Optional[str] = None  # 추가 경로가 필요한 경우

class JobUtil:
    # 클래스 레벨 변수로 큐와 스레드 관리
    _update_queues: Dict[str, queue.Queue] = {}
    _worker_threads: Dict[str, threading.Thread] = {}
    _shutdown_events: Dict[str, threading.Event] = {}
    _queue_lock = threading.Lock()
    _initialized = False
    
    # 설정값
    MAX_QUEUE_SIZE = 100  # 큐 최대 크기
    WORKER_TIMEOUT = 5.0  # 작업자 스레드 종료 대기 시간
    
    @classmethod
    def _initialize_cleanup(cls):
        """프로그램 종료시 자동 정리를 위한 초기화"""
        if not cls._initialized:
            # 프로그램 종료시 자동으로 모든 리소스 정리
            atexit.register(cls.cleanup_all_job_resources)
            cls._initialized = True
    
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
    def _ensure_worker_for_job(job_id: str):
        """
        특정 Job ID에 대한 작업자 스레드가 존재하는지 확인하고 없으면 생성
        
        Args:
            job_id (str): Job ID
        """
        # 자동 정리 초기화
        JobUtil._initialize_cleanup()
        
        with JobUtil._queue_lock:
            if job_id not in JobUtil._update_queues:
                # 큐와 이벤트 생성 (크기 제한 적용)
                JobUtil._update_queues[job_id] = queue.Queue(maxsize=JobUtil.MAX_QUEUE_SIZE)
                JobUtil._shutdown_events[job_id] = threading.Event()
                
                # 작업자 스레드 시작
                worker_thread = threading.Thread(
                    target=JobUtil._update_worker,
                    args=(job_id,),
                    name=f"JobUpdateWorker-{job_id}",
                    daemon=True
                )
                worker_thread.start()
                JobUtil._worker_threads[job_id] = worker_thread
                
                print(f"[Job Queue] Job ID {job_id}에 대한 업데이트 큐 및 작업자 스레드 생성됨")

    @staticmethod
    def _update_worker(job_id: str):
        """
        Job별 Firebase 업데이트 작업자 스레드
        
        Args:
            job_id (str): 처리할 Job ID
        """
        print(f"[Job Worker] Job ID {job_id} 업데이트 작업자 스레드 시작")
        
        update_queue = JobUtil._update_queues[job_id]
        shutdown_event = JobUtil._shutdown_events[job_id]
        
        processed_count = 0
        
        try:
            while not shutdown_event.is_set():
                try:
                    # 큐에서 업데이트 요청 가져오기 (타임아웃 1초)
                    update_request = update_queue.get(timeout=1.0)
                    
                    if update_request is None:  # 종료 신호
                        print(f"[Job Worker] Job ID {job_id} 종료 신호 수신")
                        break
                    
                    # Firebase 업데이트 실행
                    JobUtil._execute_firebase_update(update_request)
                    processed_count += 1
                    
                    update_queue.task_done()
                    
                except queue.Empty:
                    # 타임아웃 - 계속 루프
                    continue
                except Exception as e:
                    print(f"[Job Worker Error] Job ID {job_id} 업데이트 처리 중 오류: {str(e)}")
                    
        except Exception as e:
            print(f"[Job Worker Fatal] Job ID {job_id} 작업자 스레드 치명적 오류: {str(e)}")
        
        finally:
            print(f"[Job Worker] Job ID {job_id} 업데이트 작업자 스레드 종료 (처리된 요청: {processed_count}개)")

    @staticmethod
    def _execute_firebase_update(update_request: UpdateRequest):
        """
        Firebase 업데이트 실행
        
        Args:
            update_request (UpdateRequest): 업데이트 요청
        """
        try:
            firebase_system = FirebaseSystem.instance()
            job_id = update_request.state.inputs.jobId
            
            # 기본 경로 구성
            base_path = f"jobs/eventstorming_generator/{job_id}"
            if update_request.path_suffix:
                path = f"{base_path}/{update_request.path_suffix}"
            else:
                path = base_path
            
            # 업데이트 데이터 준비
            data = {
                "state": JsonUtil.convert_to_json(update_request.state),
                "lastUpdated": update_request.timestamp
            }
            
            # 업데이트 타입에 따른 처리
            if update_request.operation_type == "set":
                firebase_system.set_data(path, data)
            elif update_request.operation_type == "update":
                firebase_system.update_data(path, data)
            elif update_request.operation_type == "delete":
                firebase_system.delete_data(path)
            
            # 성공 로그는 상세 디버깅이 필요한 경우에만 출력
            # print(f"[Firebase Update] Job ID {job_id} {update_request.operation_type} 성공")
            
        except Exception as e:
            print(f"[Firebase Update Error] Job ID {update_request.state.inputs.jobId} 업데이트 실행 실패: {str(e)}")

    @staticmethod
    def _add_update_to_queue(state: State, operation_type: str, path_suffix: Optional[str] = None):
        """
        업데이트 요청을 큐에 추가
        
        Args:
            state (State): 상태 객체
            operation_type (str): 업데이트 타입 ('set', 'update', 'delete')
            path_suffix (str, optional): 추가 경로
        """
        job_id = state.inputs.jobId
        
        if not JobUtil.is_valid_job_id(job_id):
            print(f"[Job Queue Error] 유효하지 않은 Job ID: {job_id}")
            return
        
        # 작업자가 없으면 생성
        JobUtil._ensure_worker_for_job(job_id)
        
        # 업데이트 요청 생성
        update_request = UpdateRequest(
            state=state,
            timestamp=time.time(),
            operation_type=operation_type,
            path_suffix=path_suffix
        )
        
        # 큐에 추가
        try:
            JobUtil._update_queues[job_id].put(update_request, timeout=2.0)
        except queue.Full:
            print(f"[Job Queue Warning] Job ID {job_id} 큐가 가득참 - 업데이트 요청 무시됨")
        except KeyError:
            print(f"[Job Queue Error] Job ID {job_id} 큐가 존재하지 않음")
        except Exception as e:
            print(f"[Job Queue Error] 큐 추가 실패: {str(e)}")

    @staticmethod
    def get_queue_status(job_id: str) -> Dict[str, any]:
        """
        특정 Job의 큐 상태 조회
        
        Args:
            job_id (str): Job ID
            
        Returns:
            Dict[str, any]: 큐 상태 정보
        """
        with JobUtil._queue_lock:
            status = {
                "exists": job_id in JobUtil._update_queues,
                "queue_size": 0,
                "worker_alive": False,
                "shutdown_requested": False
            }
            
            if job_id in JobUtil._update_queues:
                status["queue_size"] = JobUtil._update_queues[job_id].qsize()
            
            if job_id in JobUtil._worker_threads:
                status["worker_alive"] = JobUtil._worker_threads[job_id].is_alive()
            
            if job_id in JobUtil._shutdown_events:
                status["shutdown_requested"] = JobUtil._shutdown_events[job_id].is_set()
            
            return status

    @staticmethod
    def cleanup_job_resources(job_id: str):
        """
        특정 Job의 리소스 정리 (큐, 스레드 등)
        
        Args:
            job_id (str): 정리할 Job ID
        """
        with JobUtil._queue_lock:
            if job_id in JobUtil._shutdown_events:
                print(f"[Job Cleanup] Job ID {job_id} 리소스 정리 시작")
                
                # 종료 이벤트 설정
                JobUtil._shutdown_events[job_id].set()
                
                # 큐에 종료 신호 추가 (None)
                if job_id in JobUtil._update_queues:
                    try:
                        # 남은 큐 작업들 처리 완료 대기 (최대 2초)
                        queue_obj = JobUtil._update_queues[job_id]
                        
                        # 종료 신호 추가
                        queue_obj.put(None, timeout=1.0)
                        
                        # 큐 비우기 (처리되지 않은 요청들 제거)
                        while not queue_obj.empty():
                            try:
                                queue_obj.get_nowait()
                                queue_obj.task_done()
                            except queue.Empty:
                                break
                    except:
                        pass
                
                # 스레드 종료 대기
                if job_id in JobUtil._worker_threads:
                    worker_thread = JobUtil._worker_threads[job_id]
                    worker_thread.join(timeout=JobUtil.WORKER_TIMEOUT)
                    if worker_thread.is_alive():
                        print(f"[Job Cleanup Warning] Job ID {job_id} 작업자 스레드가 {JobUtil.WORKER_TIMEOUT}초 내에 종료되지 않음")
                
                # 리소스 정리
                JobUtil._update_queues.pop(job_id, None)
                JobUtil._worker_threads.pop(job_id, None)
                JobUtil._shutdown_events.pop(job_id, None)
                
                print(f"[Job Cleanup] Job ID {job_id} 리소스 정리 완료")

    @staticmethod
    def cleanup_all_job_resources():
        """
        모든 Job의 리소스 정리
        """
        print("[Job Cleanup] 모든 Job 리소스 정리 시작")
        
        with JobUtil._queue_lock:
            job_ids = list(JobUtil._shutdown_events.keys())
        
        for job_id in job_ids:
            try:
                JobUtil.cleanup_job_resources(job_id)
            except Exception as e:
                print(f"[Job Cleanup Error] Job ID {job_id} 정리 중 오류: {str(e)}")
        
        print("[Job Cleanup] 모든 Job 리소스 정리 완료")

    @staticmethod
    def get_all_job_status() -> Dict[str, Dict[str, any]]:
        """
        모든 활성 Job의 상태 조회
        
        Returns:
            Dict[str, Dict[str, any]]: 모든 Job의 상태 정보
        """
        with JobUtil._queue_lock:
            job_ids = list(JobUtil._update_queues.keys())
        
        return {job_id: JobUtil.get_queue_status(job_id) for job_id in job_ids}

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
        새로운 작업을 Firebase에 큐 기반으로 안전하게 업로드
        
        Args:
            state (State): 업로드할 상태 객체
        """
        JobUtil._add_update_to_queue(state, "set")

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
        작업 상태를 Firebase에 큐 기반으로 안전하게 업데이트
        
        Args:
            state (State): 업데이트할 상태 객체
        """
        JobUtil._add_update_to_queue(state, "update")

    @staticmethod
    async def find_unprocessed_jobs_async() -> list:
        """
        Firebase에서 isProcessed가 false인 Job들을 비동기로 찾아서 반환
        
        Returns:
            list: 미처리 Job ID 리스트
        """
        try:
            firebase_system = FirebaseSystem.instance()
            jobs_data = await firebase_system.get_children_data_async("requestedJobs/eventstorming_generator")
            
            if not jobs_data:
                return []
            
            unprocessed_jobs = []
            for job_id, job_data in jobs_data.items():
                # Job ID 유효성 검증
                if not JobUtil.is_valid_job_id(job_id):
                    print(f"유효하지 않은 Job ID 발견: {job_id}")
                    firebase_system.delete_data_fire_and_forget(f"requestedJobs/eventstorming_generator/{job_id}")
                    continue
                
                unprocessed_jobs.append(job_id)
            
            return unprocessed_jobs
        
        except Exception as e:
            print(f"비동기 미처리 Job 검색 실패: {str(e)}")
            return []

    @staticmethod
    async def process_job_async(job_id: str, process_function: Callable) -> bool:
        """
        특정 Job을 비동기로 처리 (백그라운드 태스크로 실행하여 논블로킹)
        
        Args:
            job_id (str): 처리할 Job ID
            process_function (Callable): 비동기 처리 함수
            
        Returns:
            bool: 처리 시작 성공 여부
        """
        job_path = f"requestedJobs/eventstorming_generator/{job_id}"
        
        try:
            # Job ID 유효성 검증
            if not JobUtil.is_valid_job_id(job_id):
                print(f"유효하지 않은 Job ID: {job_id}")
                return False
            
            firebase_system = FirebaseSystem.instance()
            
            # 현재 Job 데이터 조회
            job_data = firebase_system.get_data(job_path)
            if not job_data:
                print(f"Job 데이터를 찾을 수 없음: {job_id}")
                return False
            
            # state 데이터 로그 출력
            state = job_data.get("state")   
            if not state:
                print(f"[Job 처리] Job ID: {job_id} - State 데이터 변환 실패")
                return False
            
            state = State(**state)
            state.inputs.jobId = job_id

            # Job을 백그라운드 태스크로 시작 (논블로킹)
            asyncio.create_task(JobUtil._execute_job_background(job_id, state, process_function))
            
            # requestedJobs에서 즉시 삭제 (중복 처리 방지)
            firebase_system.delete_data_fire_and_forget(job_path)
            
            return True
        
        except Exception as e:
            print(f"Job 처리 시작 중 오류 발생 (Job ID: {job_id}): {str(e)}")
            return False

    @staticmethod
    async def _execute_job_background(job_id: str, state: State, process_function: Callable):
        """
        백그라운드에서 실제 Job 처리를 수행하는 내부 함수
        
        Args:
            job_id (str): Job ID
            state (State): 처리할 상태 객체
            process_function (Callable): 비동기 처리 함수
        """
        try:
            print(f"[Job 시작] Job ID: {job_id}")
            await process_function(state)
        except Exception as e:
            print(f"[Job 백그라운드 처리 오류] Job ID: {job_id}, 오류: {str(e)}")

    @staticmethod
    async def process_all_unprocessed_jobs_async(process_function: Callable) -> int:
        """
        모든 미처리 Job들을 비동기로 찾아서 처리 (논블로킹)
        
        Args:
            process_function (Callable): 비동기 처리 함수
            
        Returns:
            int: 처리 시작된 Job 개수
        """
        try:
            unprocessed_jobs = await JobUtil.find_unprocessed_jobs_async()
            
            if not unprocessed_jobs:
                return 0
            
            print(f"[Job 모니터링] {len(unprocessed_jobs)}개의 미처리 Job 발견")
            
            # 모든 Job을 동시에 백그라운드 태스크로 시작
            tasks = [JobUtil.process_job_async(job_id, process_function) for job_id in unprocessed_jobs]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            started_count = sum(1 for result in results if result is True)
            
            print(f"[Job 모니터링] 총 {started_count}개의 Job 처리 시작")
            return started_count
        
        except Exception as e:
            print(f"비동기 미처리 Job 일괄 처리 중 오류 발생: {str(e)}")
            return 0