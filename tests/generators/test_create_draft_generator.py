from eventstorming_generator.models import CreateDraftGeneratorOutput
from eventstorming_generator.terminal.commons.generator import execute_create_draft_generator

class TestCreateDraftGenerator:
    """CreateDraftGenerator 클래스의 테스트"""
    def test_create_draft_generator(self):
        """CreateDraftGenerator를 테스트"""
        generator_result:CreateDraftGeneratorOutput = execute_create_draft_generator(is_save_to_temp=False)
        
        # 기본 검증
        assert generator_result is not None, "생성 결과가 None입니다"
        assert hasattr(generator_result, 'aggregates'), "aggregates 속성이 없습니다"
        assert isinstance(generator_result.aggregates, list), "aggregates가 리스트가 아닙니다"
        assert len(generator_result.aggregates) > 0, "최소 1개 이상의 aggregate가 필요합니다"
        
        # 각 aggregate 검증
        for idx, aggregate in enumerate(generator_result.aggregates):
            # 필수 필드 검증
            assert hasattr(aggregate, 'aggregateName'), f"Aggregate[{idx}]에 aggregateName이 없습니다"
            assert hasattr(aggregate, 'aggregateAlias'), f"Aggregate[{idx}]에 aggregateAlias가 없습니다"
            assert hasattr(aggregate, 'enumerations'), f"Aggregate[{idx}]에 enumerations가 없습니다"
            assert hasattr(aggregate, 'valueObjects'), f"Aggregate[{idx}]에 valueObjects가 없습니다"
            
            # 값 검증
            assert aggregate.aggregateName, f"Aggregate[{idx}]의 aggregateName이 비어있습니다"
            assert aggregate.aggregateAlias, f"Aggregate[{idx}]의 aggregateAlias가 비어있습니다"
            
            # PascalCase 검증 (첫 글자가 대문자인지)
            assert aggregate.aggregateName[0].isupper(), \
                f"Aggregate[{idx}]의 aggregateName이 PascalCase가 아닙니다: {aggregate.aggregateName}"
            
            # 타입 서픽스 없는지 검증
            invalid_suffixes = ['Aggregate', 'Info', 'Data', 'Entity']
            for suffix in invalid_suffixes:
                assert not aggregate.aggregateName.endswith(suffix), \
                    f"Aggregate[{idx}]의 이름에 타입 서픽스가 포함되어 있습니다: {aggregate.aggregateName}"
            
            # Enumerations 검증
            assert isinstance(aggregate.enumerations, list), \
                f"Aggregate[{idx}]의 enumerations가 리스트가 아닙니다"
            for enum_idx, enumeration in enumerate(aggregate.enumerations):
                assert hasattr(enumeration, 'name'), \
                    f"Aggregate[{idx}].Enumeration[{enum_idx}]에 name이 없습니다"
                assert hasattr(enumeration, 'alias'), \
                    f"Aggregate[{idx}].Enumeration[{enum_idx}]에 alias가 없습니다"
                assert enumeration.name, \
                    f"Aggregate[{idx}].Enumeration[{enum_idx}]의 name이 비어있습니다"
                assert enumeration.name[0].isupper(), \
                    f"Aggregate[{idx}].Enumeration[{enum_idx}]의 name이 PascalCase가 아닙니다: {enumeration.name}"
            
            # ValueObjects 검증
            assert isinstance(aggregate.valueObjects, list), \
                f"Aggregate[{idx}]의 valueObjects가 리스트가 아닙니다"
            for vo_idx, value_object in enumerate(aggregate.valueObjects):
                assert hasattr(value_object, 'name'), \
                    f"Aggregate[{idx}].ValueObject[{vo_idx}]에 name이 없습니다"
                assert hasattr(value_object, 'alias'), \
                    f"Aggregate[{idx}].ValueObject[{vo_idx}]에 alias가 없습니다"
                assert value_object.name, \
                    f"Aggregate[{idx}].ValueObject[{vo_idx}]의 name이 비어있습니다"
                assert value_object.name[0].isupper(), \
                    f"Aggregate[{idx}].ValueObject[{vo_idx}]의 name이 PascalCase가 아닙니다: {value_object.name}"
        
        # 결과 출력 (디버깅용)
        print(f"\n✓ 검증 완료: {len(generator_result.aggregates)}개의 Aggregate가 생성되었습니다")
        for aggregate in generator_result.aggregates:
            print(f"  - {aggregate.aggregateName} ({aggregate.aggregateAlias})")
            print(f"    Enumerations: {len(aggregate.enumerations)}개")
            print(f"    ValueObjects: {len(aggregate.valueObjects)}개")