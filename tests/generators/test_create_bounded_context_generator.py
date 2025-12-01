from eventstorming_generator.models import CreateBoundedContextGeneratorOutput
from eventstorming_generator.terminal.commons.generator import execute_create_bounded_context_generator

class TestCreateBoundedContextGenerator:
    """CreateBoundedContextGenerator 클래스의 테스트"""
    def test_create_bounded_context_generator(self):
        """CreateBoundedContextGenerator를 테스트"""
        generator_result:CreateBoundedContextGeneratorOutput = execute_create_bounded_context_generator(is_save_to_temp=False)

        # 기본 검증
        assert generator_result is not None, "생성 결과가 None이면 안 됩니다"
        assert hasattr(generator_result, 'boundedContexts'), "boundedContexts 속성이 존재해야 합니다"
        assert isinstance(generator_result.boundedContexts, list), "boundedContexts는 리스트여야 합니다"
        
        # Bounded Context 개수 검증 (3-15개 사이여야 함)
        bounded_contexts_count = len(generator_result.boundedContexts)
        assert 3 <= bounded_contexts_count <= 15, \
            f"Bounded Context 개수는 3-15개 사이여야 합니다. 현재: {bounded_contexts_count}개"
        
        # 각 Bounded Context 검증
        for idx, bc in enumerate(generator_result.boundedContexts):
            # 필수 필드 존재 확인
            assert hasattr(bc, 'name'), f"[{idx}] name 필드가 존재해야 합니다"
            assert hasattr(bc, 'alias'), f"[{idx}] alias 필드가 존재해야 합니다"
            assert hasattr(bc, 'importance'), f"[{idx}] importance 필드가 존재해야 합니다"
            assert hasattr(bc, 'description'), f"[{idx}] description 필드가 존재해야 합니다"
            
            # name 검증 (비어있지 않고 PascalCase 형식)
            assert bc.name, f"[{idx}] name이 비어있으면 안 됩니다"
            assert bc.name[0].isupper(), f"[{idx}] name은 PascalCase여야 합니다 (첫 글자 대문자): {bc.name}"
            assert ' ' not in bc.name, f"[{idx}] name에 공백이 있으면 안 됩니다: {bc.name}"
            
            # alias 검증 (비어있지 않음)
            assert bc.alias, f"[{idx}] alias가 비어있으면 안 됩니다"
            
            # importance 검증 (정해진 값 중 하나)
            valid_importances = ["Core Domain", "Supporting Domain", "Generic Domain"]
            assert bc.importance in valid_importances, \
                f"[{idx}] importance는 {valid_importances} 중 하나여야 합니다. 현재: {bc.importance}"
            
            # description 검증 (비어있지 않음)
            assert bc.description, f"[{idx}] description이 비어있으면 안 됩니다"
            assert len(bc.description) > 10, \
                f"[{idx}] description이 너무 짧습니다 (최소 10자 이상): {len(bc.description)}자"
        
        # 중복 이름 확인
        names = [bc.name for bc in generator_result.boundedContexts]
        assert len(names) == len(set(names)), "Bounded Context 이름이 중복되면 안 됩니다"
        
        print(f"\n✅ 검증 완료: {bounded_contexts_count}개의 Bounded Context가 생성되었습니다")
        for bc in generator_result.boundedContexts:
            print(f"  - {bc.name} ({bc.alias}) - {bc.importance}")
