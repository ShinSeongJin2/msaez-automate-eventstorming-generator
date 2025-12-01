from eventstorming_generator.config import Config
from eventstorming_generator.systems import DatabaseFactory, MemoryDBSystem
from eventstorming_generator.terminal.commons.mocks import common_requirements
from eventstorming_generator.terminal.commons.util import execute_job_request_util
from eventstorming_generator.constants import REQUEST_TYPES

class TestJobRequestUtil:
    """JobRequestUtil 클래스의 테스트"""
    def test_add_job_request_by_requirements(self):
        """requirements를 추가하고 올바른 구조를 가지고 있는지 테스트"""
        Config.set_db_type("memory")
        db_system: MemoryDBSystem = DatabaseFactory.get_db_system()
        db_system.clear()

        requirements = common_requirements.get("library_requirements")
        link = execute_job_request_util("library_requirements")
        assert link is not None
        assert "jobId=" in link

        # jobId 추출
        job_id = link.split("jobId=")[1].split("&")[0] if "&" in link.split("jobId=")[1] else link.split("jobId=")[1]

        db_data = db_system.get_all_data()
        
        # === db_data 구조 검증 시작 ===
        
        # 1. 최상위 구조 검증
        assert db_data is not None, "db_data가 None입니다"
        assert "jobs" in db_data, "db_data에 'jobs' 키가 없습니다"
        assert "requestedJobs" in db_data, "db_data에 'requestedJobs' 키가 없습니다"
        
        # 2. jobs 구조 검증
        jobs = db_data["jobs"]
        assert jobs is not None, "jobs가 None입니다"
        
        # 네임스페이스 키 찾기 (예: eventstorming_generator_local_shin)
        namespace_keys = list(jobs.keys())
        assert len(namespace_keys) > 0, "jobs에 네임스페이스 키가 없습니다"
        
        namespace = jobs[namespace_keys[0]]
        assert job_id in namespace, f"jobs.{namespace_keys[0]}에 job_id '{job_id}'가 없습니다"
        
        job_data = namespace[job_id]
        assert "state" in job_data, f"job_data에 'state' 키가 없습니다"
        assert "lastUpdated" in job_data, f"job_data에 'lastUpdated' 키가 없습니다"
        assert isinstance(job_data["lastUpdated"], (int, float)), "lastUpdated가 숫자 타입이 아닙니다"
        
        # 3. state 구조 검증
        state = job_data["state"]
        assert "inputs" in state, "state에 'inputs' 키가 없습니다"
        assert "subgraphs" in state, "state에 'subgraphs' 키가 없습니다"
        assert "outputs" in state, "state에 'outputs' 키가 없습니다"
        
        # 4. inputs 구조 검증
        inputs = state["inputs"]
        assert "requestType" in inputs, "inputs에 'requestType' 키가 없습니다"
        assert inputs["requestType"] == REQUEST_TYPES.FROM_REQUIREMENTS, \
            f"requestType이 '{REQUEST_TYPES.FROM_REQUIREMENTS}'가 아닙니다"
        
        assert "jobId" in inputs, "inputs에 'jobId' 키가 없습니다"
        assert inputs["jobId"] == job_id, f"inputs.jobId가 '{job_id}'와 일치하지 않습니다"
        
        assert "ids" in inputs, "inputs에 'ids' 키가 없습니다"
        ids = inputs["ids"]
        assert "uid" in ids, "ids에 'uid' 키가 없습니다"
        assert "projectId" in ids, "ids에 'projectId' 키가 없습니다"
        assert ids["uid"].startswith("temp-uid-"), "uid가 'temp-uid-'로 시작하지 않습니다"
        assert ids["projectId"].startswith("temp-project-id-"), "projectId가 'temp-project-id-'로 시작하지 않습니다"
        
        assert "requirements" in inputs, "inputs에 'requirements' 키가 없습니다"
        assert inputs["requirements"] == requirements, "inputs.requirements가 전달된 requirements와 일치하지 않습니다"
        
        assert "preferedLanguage" in inputs, "inputs에 'preferedLanguage' 키가 없습니다"
        assert inputs["preferedLanguage"] in ["Korean", "English"], \
            "preferedLanguage가 'Korean' 또는 'English'가 아닙니다"
        # 한글이 포함된 requirements이므로 Korean이어야 함
        assert inputs["preferedLanguage"] == "Korean", \
            "한글 requirements에 대해 preferedLanguage가 'Korean'이 아닙니다"
        
        # 5. subgraphs 구조 검증 (필수 서브그래프 모델들이 있는지 확인)
        subgraphs = state["subgraphs"]
        expected_subgraphs = [
            "createBoundedContextByFunctionsModel",
            "createAggregateByFunctionsModel",
            "createAggregateClassIdByDraftsModel",
            "createElementNamesByDraftsModel",
            "createCommandActionsByFunctionModel",
            "createPolicyActionsByFunctionModel",
            "createGwtGeneratorByFunctionModel",
            "createUiComponentsModel",
            "esValueSummaryGeneratorModel"
        ]
        
        for subgraph_name in expected_subgraphs:
            assert subgraph_name in subgraphs, f"subgraphs에 '{subgraph_name}' 키가 없습니다"
            subgraph = subgraphs[subgraph_name]
            assert isinstance(subgraph, dict), f"{subgraph_name}이 딕셔너리가 아닙니다"
        
        # 6. outputs 구조 검증
        outputs = state["outputs"]
        assert "esValue" in outputs, "outputs에 'esValue' 키가 없습니다"
        es_value = outputs["esValue"]
        assert "elements" in es_value, "esValue에 'elements' 키가 없습니다"
        assert "relations" in es_value, "esValue에 'relations' 키가 없습니다"
        assert isinstance(es_value["elements"], dict), "esValue.elements가 딕셔너리가 아닙니다"
        assert isinstance(es_value["relations"], dict), "esValue.relations가 딕셔너리가 아닙니다"
        
        assert "isCompleted" in outputs, "outputs에 'isCompleted' 키가 없습니다"
        assert "isFailed" in outputs, "outputs에 'isFailed' 키가 없습니다"
        assert "logs" in outputs, "outputs에 'logs' 키가 없습니다"
        assert isinstance(outputs["logs"], list), "outputs.logs가 리스트가 아닙니다"
        
        assert "totalProgressCount" in outputs, "outputs에 'totalProgressCount' 키가 없습니다"
        assert "currentProgressCount" in outputs, "outputs에 'currentProgressCount' 키가 없습니다"
        assert isinstance(outputs["totalProgressCount"], int), "totalProgressCount가 정수가 아닙니다"
        assert isinstance(outputs["currentProgressCount"], int), "currentProgressCount가 정수가 아닙니다"
        
        # 7. requestedJobs 구조 검증
        requested_jobs = db_data["requestedJobs"]
        assert namespace_keys[0] in requested_jobs, \
            f"requestedJobs에 네임스페이스 '{namespace_keys[0]}' 키가 없습니다"
        
        requested_namespace = requested_jobs[namespace_keys[0]]
        assert job_id in requested_namespace, \
            f"requestedJobs.{namespace_keys[0]}에 job_id '{job_id}'가 없습니다"
        
        requested_job_data = requested_namespace[job_id]
        assert "createdAt" in requested_job_data, "requested_job_data에 'createdAt' 키가 없습니다"
        assert isinstance(requested_job_data["createdAt"], (int, float)), \
            "createdAt가 숫자 타입이 아닙니다"
        
        print(f"✅ 모든 db_data 구조 검증이 성공적으로 완료되었습니다 (job_id: {job_id})")
