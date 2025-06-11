import asyncio
from eventstorming_generator.utils.job_distributor import JobDistributor
from eventstorming_generator.utils.job_util import JobUtil

async def main():
    unprocessed_jobs = await JobUtil.find_unprocessed_jobs_async()
    print(unprocessed_jobs) # ['4cc57fcc-21bd-ccee-5808-a1aabcde96f5']

    active_pod_infos = await JobDistributor.get_active_pod_infos()
    print(active_pod_infos) # [{'last_heartbeat': 1749611765.5671308, 'pod_id': 'local_pod', 'registered_at': 1749611643.7629657, 'status': 'active', 'assigned_jobs': [], 'current_processing': None}]

if __name__ == "__main__":
    asyncio.run(main())