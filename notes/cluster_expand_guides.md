# K8s 클러스터 확장 및 Replica 증설 가이드

## 개요
GKE 클러스터에서 애플리케이션의 replica 수를 늘리기 위해 노드를 추가 확장하는 과정과 리소스 확인 방법을 정리한 가이드입니다.

## 1. 현재 클러스터 리소스 상태 확인

### 1.1 기본 리소스 확인 명령어
```bash
# 노드 전체 상세 정보 확인
kubectl describe nodes

# 노드별 실시간 리소스 사용량 확인
kubectl top nodes

# 모든 파드의 리소스 사용량 확인
kubectl top pods -A

# 노드별 할당 가능한 리소스 확인
kubectl get nodes -o custom-columns=NAME:.metadata.name,ALLOCATABLE-CPU:.status.allocatable.cpu,ALLOCATABLE-MEMORY:.status.allocatable.memory
```

### 1.2 리소스 분석 방법
- **Allocatable**: 각 노드에서 파드가 사용할 수 있는 총 리소스
- **Requests**: 파드가 보장받는 최소 리소스 (스케줄링 기준)
- **Limits**: 파드가 사용할 수 있는 최대 리소스
- **실제 사용량**: `kubectl top` 명령어로 확인되는 현재 사용량

## 2. Replica 확장 계획 수립

### 2.1 필요 리소스 계산
현재 deployment.yaml 기준:
```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "200m"
  limits:
    memory: "256Mi"
    cpu: "300m"
```

**3개 replica 총 필요 리소스:**
- CPU requests: 600m (200m × 3)
- Memory requests: 384Mi (128Mi × 3)

### 2.2 리소스 충분성 판단
- 전체 클러스터에서 남은 CPU ≥ 600m
- 전체 클러스터에서 남은 Memory ≥ 384Mi

## 3. 클러스터 노드 확장

### 3.1 현재 클러스터 정보 확인
```bash
# 현재 컨텍스트 확인
kubectl config current-context

# 클러스터 정보 확인
kubectl cluster-info

# gcloud 클러스터 목록 확인
gcloud container clusters list

# 현재 프로젝트 확인
gcloud config get-value project
```

### 3.2 GKE 노드풀 확장
```bash
# 클러스터 이름을 정확히 확인 후 실행
gcloud container clusters resize [CLUSTER_NAME] \
  --num-nodes [NEW_NODE_COUNT] \
  --zone [ZONE_NAME]

# 예시 (우리 경우)
gcloud container clusters resize eventstorming-cluster \
  --num-nodes 2 \
  --zone asia-northeast3-a
```

### 3.3 확장 후 확인
```bash
# 노드 확장 확인
kubectl get nodes

# 새 노드의 상태 확인
kubectl describe nodes

# 전체 리소스 재확인
kubectl top nodes
```

## 4. Replica 확장 실행

### 4.1 확장 방법
**방법 1: kubectl 명령어**
```bash
kubectl scale deployment eventstorming-generator --replicas=3
```

**방법 2: YAML 파일 수정**
```yaml
# k8s/deployment.yaml
spec:
  replicas: 3
```
```bash
kubectl apply -f k8s/deployment.yaml
