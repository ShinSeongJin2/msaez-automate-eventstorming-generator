import asyncio
import time
import os
from kubernetes import client, config

from .systems import FirebaseSystem
from .config import Config
from .utils.logging_util import LoggingUtil
class SimpleAutoScaler:
    def __init__(self):
        self.namespace = Config.autoscaler_namespace()
        self.deployment_name = Config.autoscaler_deployment_name()
        self.service_name = Config.autoscaler_service_name()
        self.min_replicas = Config.autoscaler_min_replicas()
        self.max_replicas = Config.autoscaler_max_replicas()
        self.target_jobs_per_pod = Config.autoscaler_target_jobs_per_pod()  # 대기 작업 1개당 Pod 1개
        self.scale_check_interval = 60  # 60초마다 확인
        self.scale_up_cooldown = 120   # 스케일 업 후 2분 대기
        self.scale_down_cooldown = 300  # 스케일 다운 후 5분 대기
        self.last_scale_time = 0
        self.last_scale_action = None  # 'up' or 'down'
        
        # Kubernetes 클라이언트 초기화
        try:
            # Pod 내부에서 실행되는 경우
            config.load_incluster_config()
        except:
            # 로컬에서 테스트하는 경우
            config.load_kube_config()
        
        self.apps_v1 = client.AppsV1Api()
        self.core_v1 = client.CoreV1Api()
    
    def get_current_replicas(self) -> int:
        """현재 Deployment의 replicas 수 조회"""
        try:
            deployment = self.apps_v1.read_namespaced_deployment(
                name=self.deployment_name,
                namespace=self.namespace
            )
            return deployment.spec.replicas
        except Exception as e:
            LoggingUtil.exception("simple_autoscaler", f"현재 replicas 조회 실패: {e}", e)
            return 1
    
    def set_replicas(self, target_replicas: int) -> bool:
        """Deployment의 replicas 수 변경"""
        try:
            # Deployment 조회
            deployment = self.apps_v1.read_namespaced_deployment(
                name=self.deployment_name,
                namespace=self.namespace
            )
            
            # replicas 수 변경
            deployment.spec.replicas = target_replicas
            
            # 업데이트 적용
            self.apps_v1.patch_namespaced_deployment(
                name=self.deployment_name,
                namespace=self.namespace,
                body=deployment
            )
            
            LoggingUtil.debug("simple_autoscaler", f"Deployment replicas를 {target_replicas}개로 변경")
            return True
            
        except Exception as e:
            LoggingUtil.exception("simple_autoscaler", f"replicas 변경 실패: {e}", e)
            return False
    
    def calculate_desired_replicas(self, waiting_jobs: int) -> int:
        """대기 작업 수에 따른 목표 replicas 계산"""
        if waiting_jobs == 0:
            return self.min_replicas
        
        # 대기 작업 수 / 작업당 Pod 수로 계산
        desired = max(1, (waiting_jobs + self.target_jobs_per_pod - 1) // self.target_jobs_per_pod)
        
        # min/max 범위 내로 제한
        return max(self.min_replicas, min(self.max_replicas, desired))
    
    def should_scale(self, current_replicas: int, desired_replicas: int) -> bool:
        """스케일링이 필요한지 확인 (쿨다운 시간 고려)"""
        if current_replicas == desired_replicas:
            return False
        
        current_time = time.time()
        time_since_last_scale = current_time - self.last_scale_time
        
        # 스케일 업의 경우
        if desired_replicas > current_replicas:
            if self.last_scale_action == 'up' and time_since_last_scale < self.scale_up_cooldown:
                LoggingUtil.debug("simple_autoscaler", f"스케일 업 쿨다운 중 (남은 시간: {self.scale_up_cooldown - time_since_last_scale:.0f}초)")
                return False
        
        # 스케일 다운의 경우
        elif desired_replicas < current_replicas:
            if self.last_scale_action == 'down' and time_since_last_scale < self.scale_down_cooldown:
                LoggingUtil.debug("simple_autoscaler", f"스케일 다운 쿨다운 중 (남은 시간: {self.scale_down_cooldown - time_since_last_scale:.0f}초)")
                return False
        
        return True
    
    def is_leader_pod(self) -> bool:
        """현재 Pod가 리더인지 확인 (가장 먼저 생성된 Pod가 리더)"""
        try:
            pod_name = os.getenv('POD_ID') or os.getenv('HOSTNAME', 'unknown')
            
            # 같은 라벨을 가진 모든 Pod 조회
            pods = self.core_v1.list_namespaced_pod(
                namespace=self.namespace,
                label_selector=f"app={self.deployment_name}"
            )
            
            if not pods.items:
                return False
            
            # 생성 시간순으로 정렬하여 가장 오래된 Pod가 리더
            sorted_pods = sorted(pods.items, key=lambda p: p.metadata.creation_timestamp)
            leader_pod_name = sorted_pods[0].metadata.name
            
            is_leader = pod_name == leader_pod_name
            if is_leader:
                LoggingUtil.debug("simple_autoscaler", f"현재 Pod({pod_name})가 리더입니다")
            
            return is_leader
            
        except Exception as e:
            LoggingUtil.exception("simple_autoscaler", f"리더 확인 실패: {e}", e)
            return False
    
    async def run_autoscaling_loop(self):
        """자동 스케일링 메인 루프"""
        LoggingUtil.info("simple_autoscaler", "자동 스케일링 시작")
        
        while True:
            try:
                # 리더 Pod만 스케일링 담당
                if not self.is_leader_pod():
                    await asyncio.sleep(self.scale_check_interval)
                    continue
                
                # 대기 작업 수 조회
                waiting_jobs = await self.get_waiting_jobs_count_async()
                
                # 현재 replicas 수 조회
                current_replicas = self.get_current_replicas()
                
                # 목표 replicas 계산
                desired_replicas = self.calculate_desired_replicas(waiting_jobs)
                
                LoggingUtil.debug("simple_autoscaler", f"대기 작업: {waiting_jobs}개, 현재 Pod: {current_replicas}개, 목표 Pod: {desired_replicas}개")
                
                # 스케일링 필요성 확인
                if self.should_scale(current_replicas, desired_replicas):
                    success = self.set_replicas(desired_replicas)
                    
                    if success:
                        self.last_scale_time = time.time()
                        self.last_scale_action = 'up' if desired_replicas > current_replicas else 'down'
                        LoggingUtil.debug("simple_autoscaler", f"스케일링 완료: {current_replicas} -> {desired_replicas}")
                    else:
                        LoggingUtil.warning("simple_autoscaler", f"스케일링 실패")
                else:
                    LoggingUtil.debug("simple_autoscaler", f"스케일링 불필요 또는 쿨다운 중")
                
                await asyncio.sleep(self.scale_check_interval)
                
            except Exception as e:
                LoggingUtil.exception("simple_autoscaler", f"자동 스케일링 오류: {e}", e)
                await asyncio.sleep(self.scale_check_interval)

    async def get_waiting_jobs_count_async(self):
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
            LoggingUtil.exception("simple_autoscaler", "대기 작업 수 계산 오류", e)
            return 0

# 전역 AutoScaler 인스턴스
autoscaler = SimpleAutoScaler()

async def start_autoscaler():
    """자동 스케일러 시작"""
    await autoscaler.run_autoscaling_loop() 