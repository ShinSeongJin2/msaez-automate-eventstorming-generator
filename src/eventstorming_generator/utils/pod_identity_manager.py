from typing import Dict
import os

class PodIdentityManager:
    def __init__(self):
        self.pod_id = os.getenv('POD_NAME')
        
        if not self.pod_id:
            raise ValueError("POD_NAME 환경변수가 설정되지 않았습니다")
    
    def get_pod_info(self) -> Dict[str, str]:
        return {
            "pod_id": self.pod_id
        }