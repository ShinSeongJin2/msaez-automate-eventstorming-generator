from eventstorming_generator.models import MergeDraftGeneratorOutput
from eventstorming_generator.terminal.commons.generator import execute_merge_draft_generator

class TestMergeDraftGenerator:
    """MergeDraftGenerator 클래스의 테스트"""
    def test_merge_draft_generator(self):
        """MergeDraftGenerator를 테스트"""
        generator_result:MergeDraftGeneratorOutput = execute_merge_draft_generator(is_save_to_temp=False)
        
        # 검증: mergedDrafts가 존재하고 targetBoundedContextNames에 있는 것만 포함
        assert generator_result.mergedDrafts is not None
        assert len(generator_result.mergedDrafts) == 1
        assert generator_result.mergedDrafts[0].boundedContextName == "EnrollmentManagement"
        
        # 검증: Enrollment aggregate가 존재
        enrollment_context = generator_result.mergedDrafts[0]
        assert len(enrollment_context.aggregates) > 0