# 간단한 자동 스케일링 배포 가이드

## 📋 개요

Firebase 작업 큐의 대기 작업 수에 따라 Pod를 1~3개 사이에서 자동으로 스케일링하는 **간단한** 시스템입니다.

### 아키텍처 (매우 간단!)
```
Firebase 작업 큐 
    ↓
EventStorming Generator Pod (리더) 
    ↓ (내장된 자동 스케일러)
Kubernetes Deployment 
    ↓ (replicas 직접 조정)
Pod 자동 증감 (1~3개)
```

### 🎯 **핵심 특징**
- **추가 Pod 없음**: 기존 EventStorming Generator Pod가 자동 스케일링도 담당
- **Prometheus 불필요**: Custom Metrics API나 복잡한 설정 없음
- **리더 기반**: 가장 오래된 Pod가 리더가 되어 스케일링 담당
- **직접 제어**: Kubernetes API로 Deployment의 replicas를 직접 조정

## 🚀 배포 순서 (매우 간단!)

### 1. 이미지 재빌드 (자동 스케일러 포함)

```bash
# 자동 스케일러가 포함된 이미지 빌드
docker build -t asia-northeast3-docker.pkg.dev/eventstorming-tool-db/eventstorming-repo/eventstorming-generator:latest . --no-cache

# 이미지 푸시
docker push asia-northeast3-docker.pkg.dev/eventstorming-tool-db/eventstorming-repo/eventstorming-generator:latest
```

### 2. 애플리케이션 배포

```bash
# 기존 deployment 삭제 (필요시)
kubectl delete -f k8s/deployment.yaml

# 새로운 deployment 배포 (자동 스케일링 권한 포함)
kubectl apply -f k8s/deployment.yaml
```

**끝!** 🎉 다른 설정이나 추가 서비스가 필요하지 않습니다.

## 📊 모니터링 및 검증

### 자동 스케일링 로그 확인
```bash
# EventStorming Generator Pod 로그에서 AutoScaler 메시지 확인
kubectl logs -l app=eventstorming-generator | grep AutoScaler

# 실시간 로그 모니터링
kubectl logs -f deployment/eventstorming-generator | grep -E "(AutoScaler|리더|스케일)"
```

### 메트릭 확인
```bash
# EventStorming Generator Pod의 메트릭 직접 확인
kubectl port-forward service/eventstorming-generator-service 2024:80

# 브라우저에서 http://localhost:2024/metrics/waiting-jobs 접속
# 또는 curl로 확인
curl http://localhost:2024/metrics/waiting-jobs
```

### Pod 개수 변화 확인
```bash
# Pod 개수 실시간 모니터링
kubectl get pods -l app=eventstorming-generator --watch

# Deployment 상태 확인
kubectl get deployment eventstorming-generator --watch

# replicas 수 직접 확인
kubectl get deployment eventstorming-generator -o jsonpath='{.spec.replicas}'
```

## 🧪 테스트 시나리오

### 1. 대기 작업 없을 때 (Pod 1개 유지)
```bash
# Firebase에서 대기 작업을 모두 제거하거나 완료
# 예상 결과: Pod 1개 유지
```

### 2. 대기 작업 2개 있을 때 (Pod 2개로 스케일 업)
```bash
# Firebase에 작업 2개 추가
# 예상 결과: 약 1-2분 후 Pod 2개로 증가
```

### 3. 대기 작업 5개 있을 때 (Pod 3개로 스케일 업, 최대치)
```bash
# Firebase에 작업 5개 추가
# 예상 결과: 약 1-2분 후 Pod 3개로 증가 (최대치)
```

### 4. 작업 완료 후 (Pod 1개로 스케일 다운)
```bash
# 모든 작업이 완료되어 대기 작업이 0개가 됨
# 예상 결과: 약 5분 후 Pod 1개로 감소
```

## 🔧 튜닝 가능한 설정

### HPA 동작 조정 (k8s/deployment.yaml)
```yaml
behavior:
  scaleUp:
    stabilizationWindowSeconds: 60    # 스케일 업 안정화 시간
    policies:
    - type: Percent
      value: 100                      # 한 번에 100% 증가 가능
      periodSeconds: 60
  scaleDown:
    stabilizationWindowSeconds: 300   # 스케일 다운 안정화 시간 (5분)
    policies:
    - type: Percent
      value: 50                       # 한 번에 50% 감소 가능
      periodSeconds: 60
```

### 메트릭 캐시 조정 (src/eventstorming_generator/metrics_adapter.py)
```python
self.cache_duration = 30  # 메트릭 캐시 시간 (초)
```

## ⚠️ 주의사항

### 1. 권한 설정
- 메트릭 어댑터가 Pod 정보를 조회할 수 있도록 ServiceAccount와 RBAC 설정이 중요합니다.

### 2. 네트워크 연결
- 메트릭 어댑터는 EventStorming Generator Pod들과 통신할 수 있어야 합니다.
- Pod 간 통신이 차단되어 있으면 메트릭 수집이 실패합니다.

### 3. 메트릭 수집 실패 시
- Firebase 연결 실패 시 메트릭이 0으로 반환됩니다.
- 이 경우 Pod가 최소값(1개)으로 유지됩니다.

### 4. 스케일링 지연
- HPA는 일반적으로 1-2분마다 메트릭을 확인합니다.
- 즉시 스케일링되지 않는 것이 정상입니다.

## 🐛 트러블슈팅

### 자동 스케일링이 동작하지 않는 경우
```bash
# 리더 Pod 확인 (리더만 스케일링을 담당)
kubectl logs -l app=eventstorming-generator | grep -E "(리더|leader)"

# 권한 문제 확인
kubectl logs -l app=eventstorming-generator | grep -E "(권한|permission|forbidden)"

# ServiceAccount 확인
kubectl get serviceaccount eventstorming-generator
kubectl describe clusterrolebinding eventstorming-generator
```

### 메트릭 수집 실패
```bash
# EventStorming Generator Pod 로그 확인
kubectl logs -l app=eventstorming-generator

# Firebase 연결 상태 확인
kubectl exec -it deployment/eventstorming-generator -- curl http://localhost:2024/metrics/waiting-jobs
```

### Pod가 하나도 리더가 되지 않는 경우
```bash
# Pod 생성 시간 확인
kubectl get pods -l app=eventstorming-generator -o wide

# Pod 환경변수 확인 (POD_ID 또는 HOSTNAME)
kubectl exec -it deployment/eventstorming-generator -- env | grep -E "(POD_ID|HOSTNAME)"
```

## 📈 성능 최적화

### 1. 스케일링 주기 조정 (src/eventstorming_generator/simple_autoscaler.py)
```python
self.scale_check_interval = 60  # 60초마다 확인 (더 빠른 반응이 필요하면 줄이기)
```

### 2. 쿨다운 시간 조정
```python
self.scale_up_cooldown = 120   # 스케일 업 후 2분 대기 (빠른 스케일링이 필요하면 줄이기)
self.scale_down_cooldown = 300  # 스케일 다운 후 5분 대기 (안정적인 동작을 위해 긴 시간)
```

### 3. 작업당 Pod 수 조정
```python
self.target_jobs_per_pod = 1  # 대기 작업 1개당 Pod 1개 (부하에 따라 조정 가능)
```

### 4. 리소스 제한 조정
- EventStorming Generator Pod의 리소스 요청/제한을 환경에 맞게 조정합니다.
- 자동 스케일러는 기존 Pod 내에서 실행되므로 추가 리소스가 거의 필요하지 않습니다.

---

**작성일**: 2025-01-XX  
**프로젝트**: msaez-automate-eventstorming-generator  
**방식**: 간단한 내장형 자동 스케일링 시스템 (Prometheus 불필요) 