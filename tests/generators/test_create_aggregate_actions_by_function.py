from typing import Iterable, List, Set

from eventstorming_generator.terminal.commons.mocks import create_aggregate_actions_by_function_inputs
from eventstorming_generator.models import CreateAggregateActionsByFunctionOutput
from eventstorming_generator.terminal.commons.generator import execute_create_aggregate_actions_by_function


def _assert_refs_structure(refs: List[List[List[str]]]) -> None:
    assert isinstance(refs, list) and refs, "refs는 비어 있지 않은 리스트여야 합니다."
    for span in refs:
        assert isinstance(span, list) and len(span) == 2, "각 참조 구간은 시작과 끝 정보를 포함해야 합니다."
        for point in span:
            assert isinstance(point, list) and len(point) == 2, "각 참조 포인트는 (라인, 키워드) 쌍이어야 합니다."
            line, token = point
            assert isinstance(line, str) and line.strip(), "라인 정보는 비어 있지 않은 문자열이어야 합니다."
            assert line.isdigit(), "라인 정보는 숫자로만 구성된 문자열이어야 합니다."
            assert isinstance(token, str) and token.strip(), "키워드 정보는 비어 있지 않은 문자열이어야 합니다."


def _collect_property_names(actions: Iterable) -> Set[str]:
    property_names: Set[str] = set()
    for action in actions:
        assert action.args.properties, "속성 리스트는 비어 있을 수 없습니다."
        _assert_refs_structure(action.args.refs)
        for prop in action.args.properties:
            assert prop.name, "속성 이름은 비어 있을 수 없습니다."
            assert isinstance(prop.isKey, bool), "isKey는 불리언이어야 합니다."
            assert isinstance(prop.type, str) and prop.type.strip(), "속성 타입은 비어 있지 않은 문자열이어야 합니다."
            _assert_refs_structure(prop.refs)
            property_names.add(prop.name)
    return property_names


class TestCreateAggregateActionsByFunction:
    """CreateAggregateActionsByFunction 클래스의 테스트"""

    def test_create_aggregate_actions_by_function(self) -> None:
        """CreateAggregateActionsByFunction 결과 구조 검증"""
        inputs = create_aggregate_actions_by_function_inputs
        generator_result: CreateAggregateActionsByFunctionOutput = execute_create_aggregate_actions_by_function(is_save_to_temp=False)

        assert isinstance(generator_result, CreateAggregateActionsByFunctionOutput)

        aggregate_structure = inputs.get("targetAggregateStructure", {})
        expected_aggregate_name = aggregate_structure.get("aggregateName")
        expected_aggregate_alias = aggregate_structure.get("aggregateAlias")

        aggregate_actions = {action.args.aggregateName: action for action in generator_result.aggregateActions}
        assert aggregate_actions, "집계 행위는 최소 한 개 이상 생성되어야 합니다."

        assert expected_aggregate_name in aggregate_actions, "입력에 정의된 집계가 결과에 포함되어야 합니다."
        aggregate_action = aggregate_actions[expected_aggregate_name]
        assert aggregate_action.objectType == "Aggregate"
        assert aggregate_action.ids.aggregateId, "집계 ID는 비어 있을 수 없습니다."
        if expected_aggregate_alias:
            assert aggregate_action.args.aggregateAlias == expected_aggregate_alias

        aggregate_property_names = _collect_property_names(generator_result.aggregateActions)

        value_object_actions = {action.args.valueObjectName: action for action in generator_result.valueObjectActions}
        expected_value_object_names = {
            vo.get("name")
            for vo in aggregate_structure.get("valueObjects", [])
            if vo.get("name")
        }
        assert expected_value_object_names.issubset(value_object_actions), "입력에 정의된 값 객체가 결과에 포함되어야 합니다."

        aggregate_ids = {action.ids.aggregateId for action in generator_result.aggregateActions}
        for vo_action in value_object_actions.values():
            assert vo_action.objectType == "ValueObject"
            assert vo_action.ids.valueObjectId, "값 객체 ID는 비어 있을 수 없습니다."
            assert vo_action.ids.aggregateId in aggregate_ids, "값 객체는 유효한 집계에 속해야 합니다."
            assert vo_action.args.valueObjectAlias, "값 객체 별칭은 비어 있을 수 없습니다."

        value_object_property_names = _collect_property_names(generator_result.valueObjectActions)

        attributes_to_generate = set(inputs.get("attributesToGenerate", []))
        assert attributes_to_generate.issubset(
            aggregate_property_names.union(value_object_property_names)
        ), "모든 필수 속성은 집계 또는 값 객체 속성으로 생성되어야 합니다."

        enumeration_actions = {action.args.enumerationName: action for action in generator_result.enumerationActions}
        expected_enumeration_names = {
            enum.get("name")
            for enum in aggregate_structure.get("enumerations", [])
            if enum.get("name")
        }
        assert expected_enumeration_names.issubset(enumeration_actions), "입력에 정의된 열거형이 결과에 포함되어야 합니다."

        for enum_action in enumeration_actions.values():
            assert enum_action.objectType == "Enumeration"
            assert enum_action.ids.enumerationId, "열거형 ID는 비어 있을 수 없습니다."
            assert enum_action.ids.aggregateId in aggregate_ids, "열거형은 유효한 집계에 속해야 합니다."
            assert enum_action.args.enumerationAlias, "열거형 별칭은 비어 있을 수 없습니다."
            _assert_refs_structure(enum_action.args.refs)
            assert enum_action.args.properties, "열거형 값은 최소 한 개 이상이어야 합니다."
            for enum_value in enum_action.args.properties:
                assert enum_value.name, "열거형 값 이름은 비어 있을 수 없습니다."
                _assert_refs_structure(enum_value.refs)