# SimpleAutoScaler 개선 사항

## 문제점 분석
기존 SimpleAutoScaler는 대기 중인 작업 수만을 기준으로 스케일링을 결정했습니다. 이로 인해 다음과 같은 문제가 발생했습니다:

1. **작업 진행 중 Pod 강제 삭제**: 처리 중인 작업이 있음에도 불구하고 대기 작업이 없으면 replicas를 줄여서 작업이 중단됨
2. **작업 손실**: 1-2시간 걸리는 장시간 작업이 중간에 강제 종료됨
3. **리소스 낭비**: 불안정한 스케일링으로 인한 비효율성

## 개선 방안

### 1. 처리 중인 작업 보호
- **새로운 메서드**: `get_processing_jobs_count_async()`
- **기능**: Firebase에서 현재 처리 중인 작업(`status: 'processing'`)을 실시간으로 계산
- **조건**: `assignedPodId`가 있고, 5분 이내 heartbeat가 있는 작업

### 2. 보수적 스케일링 전략
#### 스케일 업 (Scale Up)
- **조건**: 대기 + 처리 중인 작업 수가 현재 Pod 수를 초과
- **쿨다운**: 2분 (기존과 동일)

#### 스케일 다운 (Scale Down)
- **강화된 보호 조건**:
  - 처리 중인 작업이 **단 1개라도** 있으면 스케일 다운 금지
  - 기본 쿨다운: 30분 (기존 5분 → 30분)
  - 추가 유예 시간: 1시간
  - 연속 관찰 요구: 5회 (5분 간격으로 총 25분)

### 3. Graceful Shutdown 구현
#### Kubernetes 설정
```yaml
terminationGracePeriodSeconds: 7200  # 2시간
```

#### Pod 수준 Graceful Shutdown
- **신호 처리**: SIGTERM, SIGINT 신호를 감지하여 graceful shutdown 모드 진입
- **새 작업 중단**: shutdown 요청 시 새로운 작업 수락 중단
- **현재 작업 보호**: 진행 중인 작업은 완료될 때까지 대기
- **상태 알림**: Firebase에 shutdown 상태 정보 업데이트

## 핵심 개선 사항

### 1. 복합적 스케일링 결정
```python
def calculate_desired_replicas(self, waiting_jobs: int, processing_jobs: int) -> int:
    total_jobs = waiting_jobs + processing_jobs
    min_required_for_processing = processing_jobs  # 처리 중인 작업 수만큼 최소 보장
    # ...
```

### 2. 매우 보수적인 스케일 다운
```python
def should_scale_down(self, current_replicas: int, desired_replicas: int, processing_jobs: int) -> bool:
    # 처리 중인 작업이 있으면 무조건 스케일 다운 금지
    if processing_jobs > 0:
        return False
    # 5회 연속 관찰 + 1시간 유예 시간 필요
```

### 3. Graceful Shutdown 플로우
```
SIGTERM 수신 → 새 작업 중단 → 현재 작업 완료 대기 → 안전한 종료
```

## 설정값 조정

| 설정 | 기존값 | 개선값 | 이유 |
|------|--------|--------|------|
| `scale_down_cooldown` | 300초 (5분) | 1800초 (30분) | 장시간 작업 보호 |
| `scale_down_grace_period` | 없음 | 3600초 (1시간) | 추가 안전장치 |
| `required_scale_down_observations` | 없음 | 5회 | 잘못된 스케일 다운 방지 |
| `terminationGracePeriodSeconds` | 없음 | 7200초 (2시간) | 작업 완료 시간 보장 |

## 예상 효과

### 1. 작업 안정성
- ✅ 처리 중인 작업 강제 종료 방지
- ✅ 1-2시간 장시간 작업 보호
- ✅ 데이터 손실 위험 제거

### 2. 리소스 효율성
- ✅ 불필요한 스케일 다운 방지
- ✅ 안정적인 Pod 수 유지
- ✅ 재시작 비용 절약

### 3. 운영 안정성
- ✅ 예측 가능한 스케일링 동작
- ✅ 상세한 로깅으로 모니터링 개선
- ✅ Graceful shutdown으로 서비스 안정성 향상

## 모니터링 로그 예시

```
[INFO] 작업 현황 - 대기: 2개, 처리중: 1개, Pod 현황 - 설정: 3개, 활성: 3개, 목표: 3개
[INFO] 처리 중인 작업 1개가 있어 스케일 다운 금지
[INFO] Graceful shutdown: 현재 작업 job-123 완료를 기다리는 중...
[INFO] 스케일 다운 조건 충족: 5회 연속 관찰 완료
```

이러한 개선을 통해 장시간 실행되는 작업 환경에서도 안전하고 효율적인 자동 스케일링이 가능해집니다. 