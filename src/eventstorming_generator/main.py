import asyncio
import concurrent.futures
import threading
from dotenv import load_dotenv
load_dotenv()

from eventstorming_generator.utils import JobUtil, LogUtil, DecentralizedJobManager
from eventstorming_generator.graph import graph
from eventstorming_generator.models import State
from eventstorming_generator.systems.firebase_system import FirebaseSystem
from eventstorming_generator.config import Config
from eventstorming_generator.run_healcheck_server import run_healcheck_server
from eventstorming_generator.simple_autoscaler import start_autoscaler
from eventstorming_generator.utils.logging_util import LoggingUtil

async def main():
    """메인 함수 - Flask 서버, Job 모니터링, 자동 스케일러 동시 시작"""
    
    flask_thread = None
    restart_count = 0
    
    while True:
        tasks = []
        try:
            # Flask 서버 시작 (첫 실행시에만)
            if flask_thread is None:
                flask_thread = threading.Thread(target=run_healcheck_server, daemon=True)
                flask_thread.start()
                LoggingUtil.info("main", "Flask 서버가 포트 2024에서 시작되었습니다.")
                LoggingUtil.info("main", "헬스체크 엔드포인트: http://localhost:2024/ok")

            if restart_count > 0:
                LoggingUtil.info("main", f"메인 함수 재시작 중... (재시작 횟수: {restart_count})")

            pod_id = Config.get_pod_id()
            job_manager = DecentralizedJobManager(pod_id, process_job_async)
            
            if Config.is_local_run():
                tasks.append(asyncio.create_task(job_manager.start_job_monitoring()))
                LoggingUtil.info("main", "작업 모니터링이 시작되었습니다.")
            else:
                tasks.append(asyncio.create_task(start_autoscaler()))
                tasks.append(asyncio.create_task(job_manager.start_job_monitoring()))
                LoggingUtil.info("main", "자동 스케일러 및 작업 모니터링이 시작되었습니다.")
            
            await asyncio.wait(tasks)
            
        except Exception as e:
            restart_count += 1
            LoggingUtil.exception("main", f"메인 함수에서 예외 발생 (재시작 횟수: {restart_count})", e)
            
            # 실행 중인 태스크들 정리
            for task in tasks:
                if not task.done():
                    LoggingUtil.debug("main", f"태스크 취소 중: {task}")
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        LoggingUtil.debug("main", "태스크가 정상적으로 취소되었습니다.")
                    except Exception as cleanup_error:
                        LoggingUtil.exception("main", "태스크 정리 중 예외 발생", cleanup_error)

            continue

async def process_job_async(job_id: str, complete_job_func: callable):
    """비동기 Job 처리 함수"""
    
    try:
        LoggingUtil.debug("main", f"Job 시작: {job_id}")
        if not JobUtil.is_valid_job_id(job_id):
            LoggingUtil.warning("main", f"Job 처리 오류: {job_id}, 유효하지 않음")
            return
        
        job_data = FirebaseSystem.instance().get_data(Config.get_job_path(job_id))
        if not job_data:
            LoggingUtil.warning("main", f"Job 처리 오류: {job_id}, 데이터 없음")
            return

        # state 데이터 로그 출력
        state = job_data.get("state")   
        if not state:
            LoggingUtil.warning("main", f"Job 처리 오류: {job_id} - State 데이터 변환 실패")
            return False
        state = State(**state)
        state = JobUtil.add_element_ref_to_state(state)

        # 동기 함수를 스레드에서 실행
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            await loop.run_in_executor(
                executor, 
                lambda: graph.invoke(state, {"recursion_limit": 2147483647})
            )
        LoggingUtil.debug("main", f"Job 완료: {job_id}")
        
    except Exception as e:
        LoggingUtil.exception("main", f"Job 처리 오류: {job_id}", e)

        state.outputs.is_failed = True
        LogUtil.add_exception_object_log(state, f"Job 처리 오류: {job_id}", e)
        JobUtil.update_job_to_firebase_fire_and_forget(state)
        
    finally:
        # 작업 완료 후 항상 리소스 정리
        try:

            LoggingUtil.debug("main", f"Job 정리: {job_id} 리소스 정리 중...")
            JobUtil.cleanup_job_resources(job_id)
            
            job_request_path = Config.get_requested_job_path(job_id)
            FirebaseSystem.instance().delete_data_fire_and_forget(job_request_path)

            LoggingUtil.debug("main", f"Job 정리 완료: {job_id}")
            complete_job_func()

        except Exception as cleanup_error:
            LoggingUtil.exception("main", f"Job 정리 오류: {job_id}", cleanup_error)

if __name__ == "__main__":
    asyncio.run(main())