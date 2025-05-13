from ..base import BaseModelWithItem
from .create_aggregate_by_functions_model import CreateAggregateByFunctionsModel, AggregateGenerationState

class SubgraphsModel(BaseModelWithItem):
    createAggregateByFunctionsModel: CreateAggregateByFunctionsModel = CreateAggregateByFunctionsModel()

__all__ = [
    "SubgraphsModel",
    "CreateAggregateByFunctionsModel",
    "AggregateGenerationState"
]
