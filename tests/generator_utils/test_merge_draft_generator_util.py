from eventstorming_generator.models import BoundedContextStructureModel, AggregateInfoModel
from eventstorming_generator.terminal.commons.generator_util import execute_sequential_merge_drafts_safely

class TestMergeDraftGeneratorUtil:
    """MergeDraftGeneratorUtil 클래스의 테스트"""
    def test_sequential_merge_drafts_safely(self):
        """sequential_merge_drafts_safely 함수를 테스트"""
        merged_drafts = execute_sequential_merge_drafts_safely()
        
        # 1. 기본 구조 검증
        assert merged_drafts is not None, "merged_drafts는 None이 아니어야 합니다"
        assert isinstance(merged_drafts, list), "merged_drafts는 리스트여야 합니다"
        assert len(merged_drafts) > 0, "merged_drafts는 최소 하나 이상의 요소를 포함해야 합니다"
        
        # 2. 각 BoundedContextStructureModel 검증
        bc_names = set()
        all_aggregates = {}  # {bc_name: {agg_name: aggregate}}
        
        for structure in merged_drafts:
            assert isinstance(structure, BoundedContextStructureModel), f"각 요소는 BoundedContextStructureModel이어야 합니다: {type(structure)}"
            
            # 2.1 BoundedContext 정보 검증
            assert structure.boundedContextName, "boundedContextName은 비어있지 않아야 합니다"
            assert structure.boundedContextAlias, "boundedContextAlias는 비어있지 않아야 합니다"
            assert structure.boundedContextName not in bc_names, f"중복된 BoundedContext 이름: {structure.boundedContextName}"
            bc_names.add(structure.boundedContextName)
            
            # 2.2 Aggregates 검증
            assert structure.aggregates is not None, f"{structure.boundedContextName}: aggregates는 None이 아니어야 합니다"
            assert isinstance(structure.aggregates, list), f"{structure.boundedContextName}: aggregates는 리스트여야 합니다"
            
            bc_aggregate_names = set()
            all_aggregates[structure.boundedContextName] = {}
            
            for aggregate in structure.aggregates:
                assert isinstance(aggregate, AggregateInfoModel), f"각 aggregate는 AggregateInfoModel이어야 합니다"
                
                # 2.3 Aggregate 기본 정보 검증
                assert aggregate.aggregateName, f"{structure.boundedContextName}: aggregateName은 비어있지 않아야 합니다"
                assert aggregate.aggregateAlias, f"{structure.boundedContextName}: aggregateAlias는 비어있지 않아야 합니다"
                
                # 2.4 같은 BC 내 Aggregate 이름 중복 검증
                assert aggregate.aggregateName not in bc_aggregate_names, \
                    f"{structure.boundedContextName}: 중복된 Aggregate 이름: {aggregate.aggregateName}"
                bc_aggregate_names.add(aggregate.aggregateName)
                all_aggregates[structure.boundedContextName][aggregate.aggregateName] = aggregate
                
                # 2.5 Aggregate 이름이 PascalCase 영문인지 검증
                assert aggregate.aggregateName[0].isupper(), \
                    f"{aggregate.aggregateName}은 PascalCase로 시작해야 합니다"
                assert aggregate.aggregateName.replace("_", "").isascii(), \
                    f"{aggregate.aggregateName}은 영문이어야 합니다"
                
                # 2.6 Enumerations 검증
                assert aggregate.enumerations is not None, f"{aggregate.aggregateName}: enumerations는 None이 아니어야 합니다"
                for enum in aggregate.enumerations:
                    assert enum.name, f"{aggregate.aggregateName}: enumeration name은 비어있지 않아야 합니다"
                    assert enum.alias, f"{aggregate.aggregateName}: enumeration alias는 비어있지 않아야 합니다"
                    assert enum.name[0].isupper(), f"{enum.name}은 PascalCase로 시작해야 합니다"
                
                # 2.7 ValueObjects 검증
                assert aggregate.valueObjects is not None, f"{aggregate.aggregateName}: valueObjects는 None이 아니어야 합니다"
                for vo in aggregate.valueObjects:
                    assert vo.name, f"{aggregate.aggregateName}: valueObject name은 비어있지 않아야 합니다"
                    assert vo.alias, f"{aggregate.aggregateName}: valueObject alias는 비어있지 않아야 합니다"
                    assert vo.name[0].isupper(), f"{vo.name}은 PascalCase로 시작해야 합니다"
                    
                    # 2.8 Referenced Aggregate 검증 (ID Value Objects)
                    if vo.referencedAggregate:
                        assert vo.referencedAggregate.name, \
                            f"{aggregate.aggregateName}.{vo.name}: referencedAggregate.name은 비어있지 않아야 합니다"
                        assert vo.referencedAggregate.alias, \
                            f"{aggregate.aggregateName}.{vo.name}: referencedAggregate.alias는 비어있지 않아야 합니다"
                        
                        # ID Value Object 네이밍 컨벤션 검증 (일반적으로 ~Id로 끝남)
                        assert vo.name.endswith("Id") or "Id" in vo.name, \
                            f"{aggregate.aggregateName}.{vo.name}: ID Value Object는 'Id'를 포함해야 합니다"
        
        # 3. 전역 Aggregate 이름 중복 검증 (다른 BC 간)
        all_agg_names = {}
        for bc_name, aggregates in all_aggregates.items():
            for agg_name in aggregates.keys():
                if agg_name in all_agg_names:
                    # 동일한 Aggregate가 여러 BC에 있으면 안됨
                    assert False, f"Aggregate '{agg_name}'이 여러 BC에 존재합니다: {all_agg_names[agg_name]}, {bc_name}"
                all_agg_names[agg_name] = bc_name
        
        # 4. Referenced Aggregate 참조 무결성 검증
        for bc_name, aggregates in all_aggregates.items():
            for agg_name, aggregate in aggregates.items():
                for vo in aggregate.valueObjects:
                    if vo.referencedAggregate:
                        ref_agg_name = vo.referencedAggregate.name
                        # 참조된 Aggregate가 실제로 존재하는지 확인
                        assert ref_agg_name in all_agg_names, \
                            f"{bc_name}.{agg_name}.{vo.name}: 참조된 Aggregate '{ref_agg_name}'을 찾을 수 없습니다"
        
        # 5. 통계 정보 출력 (디버깅용)
        print(f"\n✅ 검증 완료:")
        print(f"  - 총 Bounded Context 수: {len(merged_drafts)}")
        print(f"  - 총 Aggregate 수: {len(all_agg_names)}")
        
        total_enums = sum(len(agg.enumerations) for bc_aggs in all_aggregates.values() for agg in bc_aggs.values())
        total_vos = sum(len(agg.valueObjects) for bc_aggs in all_aggregates.values() for agg in bc_aggs.values())
        total_id_vos = sum(
            len([vo for vo in agg.valueObjects if vo.referencedAggregate])
            for bc_aggs in all_aggregates.values() 
            for agg in bc_aggs.values()
        )
        
        print(f"  - 총 Enumeration 수: {total_enums}")
        print(f"  - 총 ValueObject 수: {total_vos}")
        print(f"  - 총 ID ValueObject 수: {total_id_vos}")
        print(f"\n📋 Bounded Contexts: {', '.join(sorted(bc_names))}")
        print(f"📦 Aggregates: {', '.join(sorted(all_agg_names.keys()))}")