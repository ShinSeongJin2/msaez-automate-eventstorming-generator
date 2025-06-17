import os

class Config:
    @staticmethod
    def get_requested_job_root_path() -> str:
        return f"requestedJobs/{Config.get_namespace()}"
            
    @staticmethod
    def get_requested_job_path(job_id: str) -> str:
        return f"{Config.get_requested_job_root_path()}/{job_id}"


    @staticmethod
    def get_job_root_path() -> str:
        return f"jobs/{Config.get_namespace()}"

    @staticmethod
    def get_job_path(job_id: str) -> str:
        return f"{Config.get_job_root_path()}/{job_id}"


    @staticmethod
    def get_namespace() -> str:
        return os.getenv('NAMESPACE')

    @staticmethod
    def get_pod_id() -> str:
        return os.getenv('POD_ID')


    @staticmethod
    def is_local_run() -> bool:
        return os.getenv('IS_LOCAL_RUN') == 'true'
    

    @staticmethod
    def autoscaler_min_replicas() -> int:
        return int(os.getenv('AUTO_SCALE_MIN_REPLICAS', '1'))

    @staticmethod
    def autoscaler_max_replicas() -> int:
        return int(os.getenv('AUTO_SCALE_MAX_REPLICAS', '3'))
    
    @staticmethod
    def autoscaler_target_jobs_per_pod() -> int:
        return int(os.getenv('AUTO_SCALE_TARGET_JOBS_PER_POD', '1'))