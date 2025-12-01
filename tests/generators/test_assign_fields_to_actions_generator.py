from eventstorming_generator.terminal.commons.mocks import assign_fields_to_actions_generator_inputs
from eventstorming_generator.models import AssignFieldsToActionsGeneratorOutput
from eventstorming_generator.terminal.commons.generator import execute_assign_fields_to_actions_generator

class TestAssignFieldsToActionsGenerator:
    """AssignFieldsToActionsGenerator 클래스의 테스트"""
    def test_assign_fields_to_actions_generator(self):
        """AssignFieldsToActionsGenerator를 테스트"""
        generator_result:AssignFieldsToActionsGeneratorOutput = execute_assign_fields_to_actions_generator(is_save_to_temp=False)

        # 기본 구조 검증
        assert generator_result is not None, "생성 결과가 None이면 안 됩니다"
        assert isinstance(generator_result, AssignFieldsToActionsGeneratorOutput), "생성 결과 타입이 올바르지 않습니다"
        assert hasattr(generator_result, "assignments"), "assignments 속성이 존재해야 합니다"
        assert hasattr(generator_result, "invalid_properties"), "invalid_properties 속성이 존재해야 합니다"

        assignments = generator_result.assignments
        invalid_properties = generator_result.invalid_properties

        assert isinstance(assignments, list), "assignments는 리스트여야 합니다"
        assert isinstance(invalid_properties, list), "invalid_properties는 리스트여야 합니다"
        assert assignments or invalid_properties, "assignments 또는 invalid_properties 중 하나는 값을 가져야 합니다"

        # 입력 데이터 기반의 동적 기대값 구성
        missing_fields = assign_fields_to_actions_generator_inputs.get("missingFields", [])
        assert isinstance(missing_fields, list), "missingFields는 리스트여야 합니다"
        missing_fields_set = set(missing_fields)
        assert missing_fields_set, "missingFields가 비어있으면 안 됩니다"

        existing_actions = assign_fields_to_actions_generator_inputs.get("existingActions", [])
        assert isinstance(existing_actions, list), "existingActions는 리스트여야 합니다"

        valid_parent_tuples = set()
        for action in existing_actions:
            object_type = action.get("objectType")
            ids = action.get("ids", {})
            args = action.get("args", {})

            if object_type == "Aggregate":
                aggregate_id = ids.get("aggregateId")
                aggregate_name = args.get("aggregateName")
                if aggregate_id and aggregate_name:
                    valid_parent_tuples.add(("Aggregate", aggregate_id, aggregate_name))
            elif object_type == "ValueObject":
                value_object_id = ids.get("valueObjectId")
                value_object_name = args.get("valueObjectName")
                if value_object_id and value_object_name:
                    valid_parent_tuples.add(("ValueObject", value_object_id, value_object_name))

        assert valid_parent_tuples, "입력 데이터에서 유효한 parent 정보를 찾을 수 없습니다"

        assigned_property_names = set()

        for assignment in assignments:
            # parent 정보 검증
            assert assignment.parent_type in {"Aggregate", "ValueObject"}, "parent_type은 Aggregate 또는 ValueObject여야 합니다"
            parent_tuple = (assignment.parent_type, assignment.parent_id, assignment.parent_name)
            assert parent_tuple in valid_parent_tuples, f"유효하지 않은 parent 정보입니다: {parent_tuple}"

            properties_to_add = getattr(assignment, "properties_to_add", [])
            assert properties_to_add, "properties_to_add가 비어있으면 안 됩니다"

            for property_assignment in properties_to_add:
                # name 검증
                assert property_assignment.name, "property name이 비어있으면 안 됩니다"
                assert property_assignment.name in missing_fields_set, "missingFields에 존재하지 않는 property가 생성되었습니다"
                assert property_assignment.name not in assigned_property_names, "동일한 property가 중복 할당되었습니다"
                assigned_property_names.add(property_assignment.name)

                # type 검증
                assert isinstance(property_assignment.type, str) and property_assignment.type.strip(), "property type은 비어있지 않은 문자열이어야 합니다"

                # refs 구조 검증
                refs = property_assignment.refs
                assert isinstance(refs, list) and refs, "refs는 비어있지 않은 리스트여야 합니다"
                for ref in refs:
                    assert isinstance(ref, list) and len(ref) == 2, "refs의 각 항목은 길이 2의 리스트여야 합니다"
                    for position in ref:
                        assert isinstance(position, list) and len(position) == 2, "refs 포지션은 길이 2의 리스트여야 합니다"
                        line_number, phrase = position
                        assert isinstance(line_number, str) and line_number.strip(), "line_number는 비어있지 않은 문자열이어야 합니다"
                        assert isinstance(phrase, str) and phrase.strip(), "phrase는 비어있지 않은 문자열이어야 합니다"

        # invalid_properties 검증
        invalid_properties_set = set(invalid_properties)
        for invalid_property in invalid_properties_set:
            assert isinstance(invalid_property, str) and invalid_property.strip(), "invalid property는 비어있지 않은 문자열이어야 합니다"
            assert invalid_property in missing_fields_set, "missingFields에 존재하지 않는 invalid property가 포함되었습니다"

        # missingFields에 대한 완전성 검증
        assert assigned_property_names.isdisjoint(invalid_properties_set), "missingFields가 assignments와 invalid_properties에 동시에 존재합니다"
        assert assigned_property_names.union(invalid_properties_set) == missing_fields_set, "missingFields가 assignments와 invalid_properties로 완전히 매핑되지 않았습니다"