import asyncio
import signal
from eventstorming_generator.utils.job_util import JobUtil

# 전역 변수로 모니터링 루프 제어
_monitoring_active = True


def main():
    """메인 함수 - Job 모니터링 시작"""
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

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
                # 미처리 Job들 비동기 처리
                processed_count = await JobUtil.process_all_unprocessed_jobs_async()
                
                if processed_count > 0:
                    print(f"[비동기 모니터링] {processed_count}개 Job 처리 완료")
                
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


if __name__ == "__main__":
    main()