import os

class Config:
    @staticmethod
    def get_requested_job_root_path() -> str:
        IS_USE_LOCAL_SERVER = os.getenv('IS_USE_LOCAL_SERVER', 'false').lower() == 'true'
        if IS_USE_LOCAL_SERVER:
            return f"requestedJobs_local/eventstorming_generator"
        else:
            return f"requestedJobs/eventstorming_generator"

    @staticmethod
    def get_requested_job_path(job_id: str) -> str:
        return f"{Config.get_requested_job_root_path()}/{job_id}"

    @staticmethod
    def get_job_root_path() -> str:
        IS_USE_LOCAL_SERVER = os.getenv('IS_USE_LOCAL_SERVER', 'false').lower() == 'true'
        if IS_USE_LOCAL_SERVER:
            return f"jobs_local/eventstorming_generator"
        else:
            return f"jobs/eventstorming_generator"
    
    @staticmethod
    def get_job_path(job_id: str) -> str:
        return f"{Config.get_job_root_path()}/{job_id}"

    @staticmethod
    def get_active_pods_root_path() -> str:
        return f"active_pods/eventstorming_generator"

    @staticmethod
    def get_active_pods_path(pod_id: str) -> str:
        return f"{Config.get_active_pods_root_path()}/{pod_id}"
