# MSAEZ AUTOMATE EVENTSTORMING GENERATOR
## 설명
기존 [MSAEZ](https://github.com/msa-ez/platform)에서 사용하는 유저 시나리오 기반 이벤트 스토밍 생성 프로세스에서 이벤트 스토밍 생성 부분을 LangGraph를 활용하여 백엔드로 자동화시키기 위한 프로젝트입니다.

## 기본 설치 및 실행
1. .env.example 파일을 참조해서 적절한 .env 파일을 생성
2. 프로젝트 루트 터미널에서 아래 명령어 실행
```bash
uv run pip install -e .
uv pip install -U "langgraph-cli[inmem]"
# grpcio 버전 호환성 문제 해결 (langgraph-api 요구사항)
uv pip install "grpcio>=1.75.1"
uv run langgraph dev
```

## Pod에서 실행
- Pod상에서 파이어베이스의 Job을 처리하기 위해서는 main.py를 실행
```bash
uv run python ./src/eventstorming_generator/main.py
```

## 터미널 활용
- terminal.py를 실행
```bash
uv run python ./src/eventstorming_generator/terminal.py
>>> help
```
