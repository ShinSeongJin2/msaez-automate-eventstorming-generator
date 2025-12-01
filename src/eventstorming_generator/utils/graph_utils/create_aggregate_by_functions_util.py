from ...models import AggregateInfoModel

class CreateAggregateByFunctionsUtil:
    @staticmethod
    def remove_id_value_objects(aggregate_structure: AggregateInfoModel) -> AggregateInfoModel:
        """
        ID ValueObject를 제거한 초안을 반환
        """
        cloned_aggregate_structure = aggregate_structure.model_copy(deep=True)
        cloned_aggregate_structure.valueObjects = [
            value_object
            for value_object in cloned_aggregate_structure.valueObjects
            if value_object.referencedAggregate is None
        ]

        return cloned_aggregate_structure