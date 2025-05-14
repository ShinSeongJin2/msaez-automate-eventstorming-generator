from ..base import BaseModelWithItem
from .create_aggregate_by_functions_model import CreateAggregateByFunctionsModel, AggregateGenerationState
from .create_aggregate_class_id_by_drafts_model import CreateAggregateClassIdByDraftsModel, ClassIdGenerationState


class SubgraphsModel(BaseModelWithItem):
    createAggregateByFunctionsModel: CreateAggregateByFunctionsModel = CreateAggregateByFunctionsModel()
    createAggregateClassIdByDraftsModel: CreateAggregateClassIdByDraftsModel = CreateAggregateClassIdByDraftsModel()

__all__ = [
    "SubgraphsModel",
    "CreateAggregateByFunctionsModel",
    "AggregateGenerationState",
    "CreateAggregateClassIdByDraftsModel",
    "ClassIdGenerationState"
]
