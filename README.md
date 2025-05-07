# MSAEZ AUTOMATE EVENTSTORMING GENERATOR
## 설명
기존 [MSAEZ](https://github.com/msa-ez/platform)에서 사용하는 유저 시나리오 기반 이벤트 스토밍 생성 프로세스에서 이벤트 스토밍 생성 부분을 LangGraph를 활용하여 백엔드로 자동화시키기 위한 프로젝트입니다.

## 설치 & 실행
1. .env.example 파일을 참조해서 적절한 .env 파일을 생성
2. 프로젝트 루트 터미널에서 아래 명령어 실행
```bash
uv run pip install -e .
uv pip install -U "langgraph-cli[inmem]"
uv run langgraph dev
```