from eventstorming_generator.utils import CreateAggregateByFunctionsUtil
from eventstorming_generator.models import AggregateInfoModel, ValueObjectInfoModel, ReferencedAggregateInfoModel

class TestCreateAggregateByFunctionsUtil:
    """CreateAggregateByFunctionsUtil 클래스의 테스트"""
    
    def test_remove_id_value_objects(self):
        aggregate = AggregateInfoModel(
            aggregateName="Order",
            aggregateAlias="주문",
            enumerations=[],
            valueObjects=[
                ValueObjectInfoModel(
                    name="OrderId",
                    alias="주문 ID",
                    referencedAggregate=ReferencedAggregateInfoModel(name="Order", alias="주문")
                ),
                ValueObjectInfoModel(
                    name="CustomerInfo",
                    alias="고객 정보",
                    referencedAggregate=None
                ),
                ValueObjectInfoModel(
                    name="ShippingInfo",
                    alias="배송 정보",
                    referencedAggregate=None
                ),
            ],
        )

        result = CreateAggregateByFunctionsUtil.remove_id_value_objects(aggregate)

        assert len(result.valueObjects) == 2
        assert all(vo.referencedAggregate is None for vo in result.valueObjects)
        assert {vo.name for vo in result.valueObjects} == {"CustomerInfo", "ShippingInfo"}