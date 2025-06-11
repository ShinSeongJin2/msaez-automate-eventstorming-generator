from ..systems import FirebaseSystem
import time
import asyncio
from ..config import Config

class PodRegistrationManager:
    def __init__(self, pod_id: str):
        self.pod_id = pod_id
        self.last_heartbeat = time.time()
    
    async def register_pod(self):
        """Pod 등록 및 주기적 heartbeat"""
        try:
            # 초기 등록
            await FirebaseSystem.instance().set_data_async(
                Config.get_active_pods_path(self.pod_id),
                {
                    "pod_id": self.pod_id,
                    "status": "active",
                    "last_heartbeat": time.time(),
                    "registered_at": time.time(),
                    "assigned_jobs": [],
                    "current_processing": None
                }
            )
            
            print(f"[Pod Registration] Pod {self.pod_id} 등록 완료")
            
            # 주기적 heartbeat 시작
            asyncio.create_task(self.heartbeat_loop())
            
        except Exception as e:
            print(f"[Pod Registration] 등록 실패: {str(e)}")
    
    async def heartbeat_loop(self):
        """30초마다 heartbeat 전송"""
        while True:
            try:
                await FirebaseSystem.instance().update_data_async(
                    Config.get_active_pods_path(self.pod_id),
                    {
                        "last_heartbeat": time.time(),
                        "status": "active"
                    }
                )
                
                await asyncio.sleep(30)
                
            except Exception as e:
                print(f"[Heartbeat] 실패: {str(e)}")
                await asyncio.sleep(60)  # 실패 시 1분 후 재시도