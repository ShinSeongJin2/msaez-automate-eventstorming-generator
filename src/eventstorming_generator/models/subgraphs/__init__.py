from ..base import BaseModelWithItem
from .create_aggregate_by_functions_model import CreateAggregateByFunctionsModel, AggregateGenerationState
from .create_aggregate_class_id_by_drafts_model import CreateAggregateClassIdByDraftsModel, ClassIdGenerationState
from .create_command_actions_by_function_model import CreateCommandActionsByFunctionModel, CommandActionGenerationState
from .create_policy_actions_by_function_model import CreatePolicyActionsByFunctionModel, PolicyActionGenerationState
from .create_gwt_generator_by_function_model import CreateGwtGeneratorByFunctionModel, GWTGenerationState
class SubgraphsModel(BaseModelWithItem):
    createAggregateByFunctionsModel: CreateAggregateByFunctionsModel = CreateAggregateByFunctionsModel()
    createAggregateClassIdByDraftsModel: CreateAggregateClassIdByDraftsModel = CreateAggregateClassIdByDraftsModel()
    createCommandActionsByFunctionModel: CreateCommandActionsByFunctionModel = CreateCommandActionsByFunctionModel()
    createPolicyActionsByFunctionModel: CreatePolicyActionsByFunctionModel = CreatePolicyActionsByFunctionModel()
    createGwtGeneratorByFunctionModel: CreateGwtGeneratorByFunctionModel = CreateGwtGeneratorByFunctionModel()

__all__ = [
    "SubgraphsModel",
    "CreateAggregateByFunctionsModel",
    "AggregateGenerationState",
    "CreateAggregateClassIdByDraftsModel",
    "ClassIdGenerationState",
    "CreateCommandActionsByFunctionModel",
    "CommandActionGenerationState",
    "CreatePolicyActionsByFunctionModel",
    "PolicyActionGenerationState",
    "CreateGwtGeneratorByFunctionModel",
    "GWTGenerationState"
]
