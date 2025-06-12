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