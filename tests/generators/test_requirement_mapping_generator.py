from eventstorming_generator.terminal.commons.mocks import requirement_mapping_generator_inputs
from eventstorming_generator.terminal.commons.generator import execute_requirement_mapping_generator
from eventstorming_generator.models import RequirementMappingGeneratorOutput

class TestRequirementMappingGenerator:
    """RequirementMappingGenerator 클래스의 테스트"""
    def test_requirement_mapping_generator(self):
        """RequirementMappingGenerator를 테스트"""
        generator_result:RequirementMappingGeneratorOutput = execute_requirement_mapping_generator(is_save_to_temp=False)
        
        # 입력 데이터 추출
        input_requirements = requirement_mapping_generator_inputs.get("requirements")
        input_bounded_contexts = requirement_mapping_generator_inputs.get("boundedContexts")
        expected_bc_names = {bc["name"] for bc in input_bounded_contexts}
        requirements_line_count = len(input_requirements.strip().split('\n'))
        
        # 기본 검증
        assert generator_result is not None, "생성 결과가 None이면 안 됩니다"
        assert hasattr(generator_result, 'contextMappings'), "contextMappings 속성이 존재해야 합니다"
        assert isinstance(generator_result.contextMappings, list), "contextMappings는 리스트여야 합니다"
        
        # Bounded Context 매핑 개수 검증
        mappings_count = len(generator_result.contextMappings)
        expected_count = len(input_bounded_contexts)
        assert mappings_count == expected_count, \
            f"모든 Bounded Context가 매핑되어야 합니다. 기대: {expected_count}개, 실제: {mappings_count}개"
        
        # 각 Context Mapping 검증
        mapped_bc_names = set()
        for idx, mapping in enumerate(generator_result.contextMappings):
            # 필수 필드 존재 확인
            assert hasattr(mapping, 'boundedContextName'), \
                f"[{idx}] boundedContextName 필드가 존재해야 합니다"
            assert hasattr(mapping, 'refs'), \
                f"[{idx}] refs 필드가 존재해야 합니다"
            
            # boundedContextName 검증
            bc_name = mapping.boundedContextName
            assert bc_name, f"[{idx}] boundedContextName이 비어있으면 안 됩니다"
            assert bc_name in expected_bc_names, \
                f"[{idx}] boundedContextName '{bc_name}'이 입력의 Bounded Context 목록에 없습니다"
            mapped_bc_names.add(bc_name)
            
            # refs 검증
            assert isinstance(mapping.refs, list), \
                f"[{idx}] {bc_name}의 refs는 리스트여야 합니다"
            
            # 각 ref 범위 검증
            for ref_idx, ref in enumerate(mapping.refs):
                assert isinstance(ref, list), \
                    f"[{idx}] {bc_name}의 refs[{ref_idx}]는 리스트여야 합니다"
                assert len(ref) == 2, \
                    f"[{idx}] {bc_name}의 refs[{ref_idx}]는 [start, end] 형식이어야 합니다. 현재 길이: {len(ref)}"
                
                start_line, end_line = ref[0], ref[1]
                
                # 정수 타입 검증
                assert isinstance(start_line, int), \
                    f"[{idx}] {bc_name}의 refs[{ref_idx}] start_line은 정수여야 합니다"
                assert isinstance(end_line, int), \
                    f"[{idx}] {bc_name}의 refs[{ref_idx}] end_line은 정수여야 합니다"
                
                # 1-based 및 범위 검증
                assert start_line >= 1, \
                    f"[{idx}] {bc_name}의 refs[{ref_idx}] start_line은 1 이상이어야 합니다. 현재: {start_line}"
                assert end_line >= 1, \
                    f"[{idx}] {bc_name}의 refs[{ref_idx}] end_line은 1 이상이어야 합니다. 현재: {end_line}"
                assert start_line <= end_line, \
                    f"[{idx}] {bc_name}의 refs[{ref_idx}] start_line({start_line})이 end_line({end_line})보다 작거나 같아야 합니다"
                assert end_line <= requirements_line_count, \
                    f"[{idx}] {bc_name}의 refs[{ref_idx}] end_line({end_line})이 요구사항 라인 수({requirements_line_count})를 초과합니다"
        
        # 모든 Bounded Context가 매핑되었는지 확인
        assert mapped_bc_names == expected_bc_names, \
            f"매핑되지 않은 Bounded Context가 있습니다. 누락: {expected_bc_names - mapped_bc_names}"
        
        # 중복된 boundedContextName 확인
        all_names = [mapping.boundedContextName for mapping in generator_result.contextMappings]
        assert len(all_names) == len(set(all_names)), \
            "boundedContextName이 중복되면 안 됩니다"
        
        print(f"\n✅ 검증 완료: {mappings_count}개의 Context Mapping이 생성되었습니다")
        for mapping in generator_result.contextMappings:
            ref_count = len(mapping.refs)
            total_lines = sum(ref[1] - ref[0] + 1 for ref in mapping.refs) if mapping.refs else 0
            print(f"  - {mapping.boundedContextName}: {ref_count}개 범위, 총 {total_lines}줄 매핑")
            if mapping.refs:
                for ref in mapping.refs:
                    print(f"      → [{ref[0]}, {ref[1]}]")