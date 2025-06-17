from flask import Flask, jsonify, request
import asyncio
from .systems import FirebaseSystem
from .config import Config

app = Flask(__name__)

@app.after_request
def after_request(response):
    """모든 응답에 CORS 헤더 추가"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/ok', methods=['GET', 'OPTIONS'])
def health_check():
    """헬스체크 엔드포인트"""
    if request.method == 'OPTIONS':
        # CORS preflight 요청 처리
        return '', 200
    
    return jsonify({
        'status': 'ok',
        'message': 'EventStorming Generator 서버가 정상 작동 중입니다.'
    })

@app.route('/metrics/waiting-jobs', methods=['GET'])
def get_waiting_jobs_metric():
    """대기 중인 작업 수를 반환하는 메트릭 엔드포인트"""
    try:
        # 비동기 함수를 동기적으로 실행
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            waiting_count = loop.run_until_complete(_get_waiting_jobs_count_async())
            
            # Prometheus 형식으로 반환 (HPA가 파싱하기 쉽도록)
            prometheus_format = f"waiting_jobs_count {waiting_count}\n"
            
            return prometheus_format, 200, {'Content-Type': 'text/plain'}
            
        finally:
            loop.close()
            
    except Exception as e:
        print(f"대기 작업 수 조회 오류: {e}")
        return f"waiting_jobs_count 0\n", 200, {'Content-Type': 'text/plain'}

async def _get_waiting_jobs_count_async():
    """대기 중인 작업 수를 비동기로 계산"""
    try:
        # Firebase에서 현재 작업 데이터 조회
        requested_jobs = await FirebaseSystem.instance().get_children_data_async(
            Config.get_requested_job_root_path()
        )
        
        if not requested_jobs:
            return 0
        
        # DecentralizedJobManager와 동일한 로직으로 대기 작업 계산
        waiting_count = 0
        for job_id, job_data in requested_jobs.items():
            # assignedPodId가 없는 작업들이 대기 중인 작업
            if job_data.get('assignedPodId') is None:
                waiting_count += 1
        
        return waiting_count
        
    except Exception as e:
        print(f"대기 작업 수 계산 오류: {e}")
        return 0

def run_healcheck_server():
    """Flask 서버를 별도 스레드에서 실행"""
    app.run(host='0.0.0.0', port=2024, debug=False, use_reloader=False)