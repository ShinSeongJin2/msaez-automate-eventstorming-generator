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
    def get_job_state_root_path() -> str:
        return f"jobStates/{Config.get_namespace()}"
    
    @staticmethod
    def get_job_state_path(job_id: str) -> str:
        return f"{Config.get_job_state_root_path()}/{job_id}"


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
    def autoscaler_namespace() -> str:
        return os.getenv('AUTO_SCALE_NAMESPACE', 'default')
    
    @staticmethod
    def autoscaler_deployment_name() -> str:
        return os.getenv('AUTO_SCALE_DEPLOYMENT_NAME', 'eventstorming-generator')
    
    @staticmethod
    def autoscaler_service_name() -> str:
        return os.getenv('AUTO_SCALE_SERVICE_NAME', 'eventstorming-generator-service')

    @staticmethod
    def autoscaler_min_replicas() -> int:
        return int(os.getenv('AUTO_SCALE_MIN_REPLICAS', '1'))

    @staticmethod
    def autoscaler_max_replicas() -> int:
        return int(os.getenv('AUTO_SCALE_MAX_REPLICAS', '3'))
    
    @staticmethod
    def autoscaler_target_jobs_per_pod() -> int:
        return int(os.getenv('AUTO_SCALE_TARGET_JOBS_PER_POD', '1'))
    

    @staticmethod
    def get_log_level() -> str:
        """환경별 로그 레벨 반환 (DEBUG, INFO, WARNING, ERROR)"""
        if Config.is_local_run():
            return os.getenv('LOG_LEVEL', 'DEBUG')  # 로컬에서는 DEBUG 기본
        else:
            return os.getenv('LOG_LEVEL', 'INFO')   # Pod에서는 INFO 기본