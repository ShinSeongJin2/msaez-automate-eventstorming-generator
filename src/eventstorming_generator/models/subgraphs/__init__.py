from ..base import BaseModelWithItem
from .create_aggregate_by_functions_model import CreateAggregateByFunctionsModel, AggregateGenerationState
from .create_aggregate_class_id_by_drafts_model import CreateAggregateClassIdByDraftsModel, ClassIdGenerationState
from .create_command_actions_by_function_model import CreateCommandActionsByFunctionModel, CommandActionGenerationState

class SubgraphsModel(BaseModelWithItem):
    createAggregateByFunctionsModel: CreateAggregateByFunctionsModel = CreateAggregateByFunctionsModel()
    createAggregateClassIdByDraftsModel: CreateAggregateClassIdByDraftsModel = CreateAggregateClassIdByDraftsModel()
    createCommandActionsByFunctionModel: CreateCommandActionsByFunctionModel = CreateCommandActionsByFunctionModel()

__all__ = [
    "SubgraphsModel",
    "CreateAggregateByFunctionsModel",
    "AggregateGenerationState",
    "CreateAggregateClassIdByDraftsModel",
    "ClassIdGenerationState",
    "CreateCommandActionsByFunctionModel",
    "CommandActionGenerationState"
]
