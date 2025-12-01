from eventstorming_generator.models import BoundedContextStructureModel
from eventstorming_generator.terminal.commons.generator_util import execute_create_draft_by_function_safely

class TestCreateDraftGeneratorUtil:
    """CreateDraftGeneratorUtil 클래스의 테스트"""
    def test_create_draft_by_function_safely(self):
        """create_draft_by_function_safely 함수를 테스트"""
        draft = execute_create_draft_by_function_safely()

        # 1. 기본 검증: draft가 생성되었는지 확인
        assert draft is not None, "Draft should not be None"
        assert isinstance(draft, BoundedContextStructureModel), "Draft should be BoundedContextStructureModel instance"
        
        # 2. BoundedContext 정보 검증
        assert draft.boundedContextName == "LoanManagement", \
            f"Expected boundedContextName 'LoanManagement', got '{draft.boundedContextName}'"
        assert draft.boundedContextAlias == "도서관 대출 관리", \
            f"Expected boundedContextAlias '도서관 대출 관리', got '{draft.boundedContextAlias}'"
        
        # 3. Aggregates 존재 여부 검증
        assert draft.aggregates is not None, "Aggregates should not be None"
        assert len(draft.aggregates) > 0, "Aggregates should not be empty"
        
        # 4. 각 Aggregate 검증
        aggregate_names = set()
        for aggregate in draft.aggregates:
            # 필수 필드 존재 검증
            assert aggregate.aggregateName, "Aggregate name should not be empty"
            assert aggregate.aggregateAlias, "Aggregate alias should not be empty"
            
            # PascalCase 네이밍 규칙 검증
            assert aggregate.aggregateName[0].isupper(), \
                f"Aggregate name '{aggregate.aggregateName}' should start with uppercase"
            assert " " not in aggregate.aggregateName, \
                f"Aggregate name '{aggregate.aggregateName}' should not contain spaces"
            
            # 중복 검증
            assert aggregate.aggregateName.lower() not in aggregate_names, \
                f"Duplicate aggregate name found: '{aggregate.aggregateName}'"
            aggregate_names.add(aggregate.aggregateName.lower())
            
            # 5. Enumeration 검증
            if aggregate.enumerations:
                enum_names = set()
                for enum in aggregate.enumerations:
                    assert enum.name, "Enumeration name should not be empty"
                    assert enum.alias, "Enumeration alias should not be empty"
                    assert enum.name[0].isupper(), \
                        f"Enumeration name '{enum.name}' should start with uppercase"
                    
                    # Enumeration 중복 검증
                    assert enum.name.lower() not in enum_names, \
                        f"Duplicate enumeration name in {aggregate.aggregateName}: '{enum.name}'"
                    enum_names.add(enum.name.lower())
            
            # 6. ValueObject 검증
            if aggregate.valueObjects:
                vo_names = set()
                for vo in aggregate.valueObjects:
                    assert vo.name, "ValueObject name should not be empty"
                    assert vo.alias, "ValueObject alias should not be empty"
                    assert vo.name[0].isupper(), \
                        f"ValueObject name '{vo.name}' should start with uppercase"
                    
                    # ValueObject 중복 검증
                    assert vo.name.lower() not in vo_names, \
                        f"Duplicate value object name in {aggregate.aggregateName}: '{vo.name}'"
                    vo_names.add(vo.name.lower())
                    
                    # referencedAggregate는 None일 수 있음
                    assert hasattr(vo, 'referencedAggregate'), \
                        "ValueObject should have referencedAggregate attribute"
        
        print(f"\n✓ Draft validation passed!")
        print(f"✓ BoundedContext: {draft.boundedContextName} ({draft.boundedContextAlias})")
        print(f"✓ Total Aggregates: {len(draft.aggregates)}")
        for agg in draft.aggregates:
            print(f"  - {agg.aggregateName} ({agg.aggregateAlias}): "
                  f"{len(agg.enumerations)} enums, {len(agg.valueObjects)} VOs")

