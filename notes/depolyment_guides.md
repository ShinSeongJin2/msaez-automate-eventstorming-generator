# 랭그래프 파이썬 프로젝트 GKE 배포 완전 가이드

## 📋 프로젝트 개요

### 프로젝트 특징
- **랭그래프 파이썬 프로젝트**: EventStorming Generator
- **주요 기능**: Firebase 작업 큐 감시 → LangGraph 실행
- **실행 방식**: `main.py` 실행으로 큐 모니터링
- **외부 의존성**: 
  - Firebase Realtime Database (작업 큐)
  - OpenAI API (LLM 통신)
  - Firebase 인증 파일 (`.auth/serviceAccountKey.json`)

### 필요한 환경변수
```env
OPENAI_API_KEY=your-api-key
FIREBASE_DATABASE_URL=your-firebase-url
FIREBASE_SERVICE_ACCOUNT_PATH=/app/.auth/serviceAccountKey.json
AI_MODEL=openai:gpt-4.1-2025-04-14
LANGSMITH_TRACING=true
LANGSMITH_PROJECT=your-project
LANGSMITH_API_KEY=your-langsmith-key
```

## 🚀 배포 및 운영 명령어

### 이미지 빌드 및 배포
```bash
# 1. 이미지 빌드
docker build -t asia-northeast3-docker.pkg.dev/eventstorming-tool-db/eventstorming-repo/eventstorming-generator:latest . --no-cache

# 2. 이미지 푸시
docker push asia-northeast3-docker.pkg.dev/eventstorming-tool-db/eventstorming-repo/eventstorming-generator:latest

# 3. Kubernetes 배포
kubectl apply -f k8s/deployment.yaml

# 4. 외부 IP 확인
kubectl get service eventstorming-generator-service -w
```

### 모니터링 명령어
```bash
# Pod 상태 확인
kubectl get pods -l app=eventstorming-generator

# 로그 확인
kubectl logs -f deployment/eventstorming-generator

# 서비스 상태 확인
kubectl get service eventstorming-generator-service

# 리소스 사용량 확인
kubectl top nodes
kubectl top pods
```

### 헬스체크 테스트
```bash
# 외부 IP로 접근 (LoadBalancer 할당 후)
curl http://35.216.xxx.xxx/ok

# 예상 응답
{
  "status": "ok",
  "message": "EventStorming Generator 서버가 정상 작동 중입니다."
}
```

## 🛠️ 최종 배포 설정

### Kubernetes Secret 생성
```bash
# Firebase 키 시크릿
kubectl create secret generic firebase-key \
  --from-file=serviceAccountKey.json=./.auth/serviceAccountKey.json

# 환경변수 시크릿
kubectl create secret generic app-secrets \
  --from-literal=AI_MODEL="openai:gpt-4.1-2025-04-14" \
  --from-literal=OPENAI_API_KEY="your-api-key" \
  --from-literal=LANGSMITH_TRACING="true" \
  --from-literal=LANGSMITH_PROJECT="your-project" \
  --from-literal=LANGSMITH_API_KEY="your-langsmith-key" \
  --from-literal=FIREBASE_SERVICE_ACCOUNT_PATH="./.auth/serviceAccountKey.json" \
  --from-literal=FIREBASE_DATABASE_URL="your-firebase-url" 
```

### 최종 deployment.yaml
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: eventstorming-generator
  labels:
    app: eventstorming-generator
spec:
  replicas: 1
  selector:
    matchLabels:
      app: eventstorming-generator
  template:
    metadata:
      labels:
        app: eventstorming-generator
    spec:
      containers:
      - name: eventstorming-generator
        image: asia-northeast3-docker.pkg.dev/eventstorming-tool-db/eventstorming-repo/eventstorming-generator:latest
        ports:
        - containerPort: 2024
        env:
        - name: AI_MODEL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: AI_MODEL
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: OPENAI_API_KEY
        - name: LANGSMITH_TRACING
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: LANGSMITH_TRACING
        - name: LANGSMITH_PROJECT
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: LANGSMITH_PROJECT
        - name: LANGSMITH_API_KEY
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: LANGSMITH_API_KEY
        - name: FIREBASE_SERVICE_ACCOUNT_PATH
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: FIREBASE_SERVICE_ACCOUNT_PATH
        - name: FIREBASE_DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: FIREBASE_DATABASE_URL
        volumeMounts:
        - name: firebase-key-volume
          mountPath: /app/.auth
          readOnly: true
        resources:
          requests:
            memory: "128Mi"
            cpu: "200m"
          limits:
            memory: "256Mi"
            cpu: "300m"
        livenessProbe:
          httpGet:
            path: /ok
            port: 2024
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ok
            port: 2024
          initialDelaySeconds: 5
          periodSeconds: 5
      volumes:
      - name: firebase-key-volume
        secret:
          secretName: firebase-key
---
apiVersion: v1
kind: Service
metadata:
  name: eventstorming-generator-service
spec:
  selector:
    app: eventstorming-generator
  ports:
    - protocol: TCP
      port: 80
      targetPort: 2024
  type: LoadBalancer
```

## 🚨 겪었던 주요 문제들과 해결책

### 1. kubectl 연결 실패
**문제**: `dial tcp [::1]:8080: connectex: No connection could be made`
```bash
kubectl create secret generic firebase-key --from-file=serviceAccountKey.json
# 연결 거부 오류 발생
```

**원인**: GKE 클러스터가 생성되지 않음

**해결책**:
```bash
# 1. GCP 로그인 및 프로젝트 설정
gcloud auth login
gcloud config set project YOUR-PROJECT-ID

# 2. API 활성화
gcloud services enable container.googleapis.com
gcloud services enable containerregistry.googleapis.com

# 3. GKE 클러스터 생성
gcloud container clusters create eventstorming-cluster \
  --zone=asia-northeast3-a \
  --num-nodes=1 \
  --machine-type=e2-medium \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=1

# 4. kubectl 연결
gcloud container clusters get-credentials eventstorming-cluster --zone=asia-northeast3-a
```

### 2. Pod Pending 상태 (CPU 리소스 부족)
**문제**: Pod가 계속 Pending 상태
```
0/1 nodes are available: 1 Insufficient cpu.
```

**원인 분석**:
```
노드 CPU 현황:
- 전체 CPU: 2 cores (e2-medium)
- 할당 가능한 CPU: 940m
- 시스템 Pod 사용량: 713m (76%)
- 남은 CPU: 227m
- 요청한 CPU: 250m → 부족!
```

**시스템 Pod들이 사용하는 CPU**:
```
kube-dns:               270m (28%)
fluentbit-gke:         105m (11%) 
kube-state-metrics:    105m (11%)
kube-proxy:            100m (10%)
기타 시스템 Pod들:      약 133m
```

**해결책**: CPU 요청량 줄이기
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "200m"     # 250m → 200m로 줄임
  limits:
    memory: "256Mi"
    cpu: "300m"     # 500m → 300m로 줄임
```

### 3. ImagePullBackOff - GCR 서비스 종료
**문제**: 이미지 푸시 실패
```
docker push gcr.io/eventstorming-tool-db/eventstorming-generator:latest
# Retrying in ... 계속 반복
```

**원인**: Google Container Registry(GCR) 서비스 종료
```
Container Registry is deprecated and shutting down, 
please use the auto migration tool to migrate to Artifact Registry
```

**해결책**: Artifact Registry로 마이그레이션
```bash
# 1. Artifact Registry API 활성화
gcloud services enable artifactregistry.googleapis.com

# 2. Repository 생성
gcloud artifacts repositories create eventstorming-repo \
  --repository-format=docker \
  --location=asia-northeast3

# 3. 인증 설정
gcloud auth configure-docker asia-northeast3-docker.pkg.dev

# 4. 이미지 재태그 및 푸시
docker tag gcr.io/eventstorming-tool-db/eventstorming-generator:latest \
  asia-northeast3-docker.pkg.dev/eventstorming-tool-db/eventstorming-repo/eventstorming-generator:latest

docker push asia-northeast3-docker.pkg.dev/eventstorming-tool-db/eventstorming-repo/eventstorming-generator:latest
```

### 4. CrashLoopBackOff - Python 모듈 경로 문제
**문제**: Pod가 시작 후 즉시 크래시
```
ModuleNotFoundError: No module named 'eventstorming_generator'
```

**원인**: Dockerfile에서 Python 모듈이 올바르게 설치되지 않음

**해결책**: Dockerfile 수정
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 시스템 의존성 설치
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Python 의존성 파일 복사
COPY pyproject.toml ./
COPY uv.lock ./

# 애플리케이션 코드 복사
COPY src/ ./src/

# uv 설치 및 의존성 설치
RUN pip install uv
RUN uv sync --frozen

# Python 경로 설정 (핵심!)
ENV PYTHONPATH=/app/src

# 포트 노출
EXPOSE 2024

# 애플리케이션 실행
CMD ["uv", "run", "python", "-m", "eventstorming_generator.main"]
```

## 📊 리소스 사용량 분석

### e2-medium 노드의 CPU 분배
```
총 CPU: 2 cores (2000m)
할당 가능: 940m (47%)
시스템 사용: 713m (76% of 940m)
애플리케이션: 200m (21% of 940m)
여유 공간: 27m (3% of 940m)
```

### 주요 시스템 Pod 리소스 사용량
| Pod | CPU 요청량 | 용도 |
|-----|------------|------|
| kube-dns | 270m | 클러스터 DNS |
| fluentbit-gke | 105m | 로그 수집 |
| kube-state-metrics | 105m | 메트릭 수집 |
| kube-proxy | 100m | 네트워크 프록시 |
| 기타 시스템 Pod | 133m | 모니터링/관리 |

## 🔒 보안 고려사항

### 시크릿 관리
- ✅ Firebase 인증 키를 Kubernetes Secret으로 관리
- ✅ API 키들을 환경변수 Secret으로 분리
- ✅ 파일 마운트를 read-only로 설정

### 네트워크 보안
- ✅ LoadBalancer로 제한된 포트만 노출 (80 → 2024)
- ✅ 헬스체크 엔드포인트만 외부 접근 허용

## 💡 학습한 내용

### Kubernetes 핵심 개념
1. **Pod**: 애플리케이션 실행 단위
2. **Deployment**: Pod 배포 관리
3. **Service**: 네트워크 접근 추상화
4. **Secret**: 민감 정보 안전 관리
5. **ConfigMap vs Secret**: 설정 vs 민감정보

### GKE 특징
- **관리형 서비스**: Google이 많은 시스템 Pod 자동 관리
- **리소스 오버헤드**: 순수 Kubernetes보다 높은 시스템 사용량
- **자동 스케일링**: 노드 자동 확장/축소 가능

### Docker 컨테이너화 핵심
- **PYTHONPATH 설정**: Python 모듈 경로 문제 해결
- **uv 패키지 관리자**: 빠른 의존성 설치
- **멀티스테이지 빌드**: 효율적인 이미지 크기 관리

## 🎯 배포 성공 지표

### ✅ 최종 성공 상태
- **Pod Status**: Running (1/1)
- **Service**: LoadBalancer with External IP
- **Health Check**: `/ok` 엔드포인트 정상 응답
- **외부 접근**: 인터넷에서 접근 가능

### 📈 성능 최적화 포인트
- **CPU 요청량**: 200m (충분한 여유 공간 확보)
- **메모리 사용량**: 128Mi 요청, 256Mi 제한
- **헬스체크**: 5초 간격으로 빠른 장애 감지

---

**작성일**: 2025-06-05  
**프로젝트**: msaez-automate-eventstorming-generator  
**배포 환경**: Google Kubernetes Engine (GKE)  
**최종 상태**: 성공적 배포 및 외부 접근 가능
