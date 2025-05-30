import asyncio
import signal
import threading

from eventstorming_generator.utils.job_util import JobUtil
from eventstorming_generator.graph import graph
from eventstorming_generator.models import State
from eventstorming_generator.run_healcheck_server import run_healcheck_server

# 전역 변수로 모니터링 루프 제어
_monitoring_active = True


def main():
    """메인 함수 - Flask 서버와 Job 모니터링 동시 시작"""
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Flask 서버를 별도 스레드에서 시작
    flask_thread = threading.Thread(target=run_healcheck_server, daemon=True)
    flask_thread.start()
    print("[시스템] Flask 서버가 포트 2024에서 시작되었습니다.")
    print("[시스템] 헬스체크 엔드포인트: http://localhost:2024/ok")

    # Job 모니터링 시작
    asyncio.run(monitor_jobs_async(5))

def signal_handler(signum, frame):
    """Ctrl+C 등의 시그널 처리"""
    global _monitoring_active
    print("\n[시스템] 종료 신호를 받았습니다. 모니터링을 중단합니다...")
    _monitoring_active = False

async def monitor_jobs_async(interval_seconds: int = 5):
    """
    비동기 방식으로 Firebase Job을 주기적으로 모니터링
    
    Args:
        interval_seconds (int): 모니터링 간격 (초)
    """
    global _monitoring_active
    
    print(f"[비동기 Job 모니터링 시작] {interval_seconds}초 간격으로 미처리 Job을 감시합니다.")
    print("[종료하려면 Ctrl+C를 누르세요]")
    
    try:
        while _monitoring_active:
            try:
                # 미처리 Job들 비동기 처리 (논블로킹)
                processed_count = await JobUtil.process_all_unprocessed_jobs_async(process_job_async)
                
                if processed_count > 0:
                    print(f"[비동기 모니터링] {processed_count}개 Job 처리 시작됨")
                
                # 다음 체크까지 비동기 대기
                await asyncio.sleep(interval_seconds)
                    
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"[비동기 모니터링 오류] {str(e)}")
                await asyncio.sleep(interval_seconds)
                
    except asyncio.CancelledError:
        pass
    
    print("\n[비동기 Job 모니터링 종료]")

async def process_job_async(state: State):
    """비동기 Job 처리 함수"""
    try:
        # graph.invoke를 별도 executor에서 실행하여 논블로킹 처리
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, graph.invoke, state)
        print(f"[Job 완료] Job ID: {state.inputs.jobId}")
    except Exception as e:
        print(f"[Job 처리 오류] Job ID: {state.inputs.jobId}, 오류: {str(e)}")

if __name__ == "__main__":
    main()