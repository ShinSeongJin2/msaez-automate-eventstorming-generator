from flask import Flask, jsonify, request

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

def run_healcheck_server():
    """Flask 서버를 별도 스레드에서 실행"""
    app.run(host='0.0.0.0', port=2024, debug=False, use_reloader=False)