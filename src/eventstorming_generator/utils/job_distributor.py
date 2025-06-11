import time
import asyncio
from typing import List

from ..config import Config
from ..systems import FirebaseSystem

class JobDistributor:
    @staticmethod
    async def get_active_pod_infos() -> List[dict]:
        """Firebase에서 활성 Pod 목록 조회"""
        try:
            pods_data = await FirebaseSystem.instance().get_children_data_async(Config.get_active_pods_root_path())
            if not pods_data:
                return []
            
            current_time = time.time()
            active_pod_infos = []
            
            for pod_id, pod_info in pods_data.items():
                # 2분 이내에 heartbeat가 있으면 활성으로 간주
                if current_time - pod_info.get("last_heartbeat", 0) < 120:
                    pod_info["assigned_jobs"] = pod_info.get("assigned_jobs", [])
                    pod_info["current_processing"] = pod_info.get("current_processing", None)
                    active_pod_infos.append(pod_info)
                else:
                    # 죽은 Pod 정리
                    asyncio.create_task(JobDistributor.cleanup_dead_pod(pod_id))
            
            return active_pod_infos
            
        except Exception as e:
            print(f"[Pod Discovery] 활성 Pod 조회 실패: {str(e)}")
            return []
    
    @staticmethod
    async def cleanup_dead_pod(pod_id: str):
        """죽은 Pod 정리"""
        try:
            await FirebaseSystem.instance().delete_data_async(Config.get_active_pods_path(pod_id))
            print(f"[Pod Cleanup] {pod_id} 정리 완료")
        except Exception as e:
            print(f"[Pod Cleanup] {pod_id} 정리 실패: {str(e)}")