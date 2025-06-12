import asyncio
import concurrent.futures

from eventstorming_generator.utils import JobUtil, DecentralizedJobManager
from eventstorming_generator.graph import graph
from eventstorming_generator.models import State
from eventstorming_generator.systems.firebase_system import FirebaseSystem
from eventstorming_generator.config import Config

async def main():
    """메인 함수 - Flask 서버와 Job 모니터링 동시 시작"""

    pod_id = Config.get_pod_id()
    job_manager = DecentralizedJobManager(pod_id, process_job_async)
    await job_manager.start_job_monitoring()
    
async def process_job_async(job_id: str, complete_job_func: callable):
    """비동기 Job 처리 함수"""
    
    try:
        print(f"[Job 시작] Job ID: {job_id}")
        if not JobUtil.is_valid_job_id(job_id):
            print(f"[Job 처리 오류] Job ID: {job_id}, 유효하지 않음")
            return
        
        job_request_path = Config.get_requested_job_path(job_id)
        job_data = FirebaseSystem.instance().get_data(job_request_path)
        if not job_data:
            print(f"[Job 처리 오류] Job ID: {job_id}, 데이터 없음")
            return

        # state 데이터 로그 출력
        state = job_data.get("state")   
        if not state:
            print(f"[Job 처리] Job ID: {job_id} - State 데이터 변환 실패")
            return False
        state = State(**state)

        # 동기 함수를 스레드에서 실행
        loop = asyncio.get_event_loop()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            await loop.run_in_executor(
                executor, 
                lambda: graph.invoke(state, {"recursion_limit": 2147483647})
            )
        print(f"[Job 완료] Job ID: {job_id}")
        
    except Exception as e:
        print(f"[Job 처리 오류] Job ID: {job_id}, 오류: {str(e)}")
        
    finally:
        # 작업 완료 후 항상 리소스 정리
        try:
            print(f"[Job 정리] Job ID {job_id} 리소스 정리 중...")
            JobUtil.cleanup_job_resources(job_id)
            
            job_request_path = Config.get_requested_job_path(job_id)
            FirebaseSystem.instance().delete_data_fire_and_forget(job_request_path)

            print(f"[Job 정리 완료] Job ID {job_id}")

            complete_job_func()
        except Exception as cleanup_error:
            print(f"[Job 정리 오류] Job ID {job_id} 리소스 정리 중 오류: {str(cleanup_error)}")

if __name__ == "__main__":
    asyncio.run(main())