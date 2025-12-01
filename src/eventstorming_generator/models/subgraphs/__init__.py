from pydantic import Field

from ..base import BaseModelWithItem
from .create_bounded_context_by_functions_model import CreateBoundedContextByFunctionsModel, BoundedContextGenerationState
from .create_context_mapping_model import CreateContextMappingModel, ContextMappingGenerationState
from .create_draft_by_function_model import CreateDraftByFunctionModel, DraftGenerationState
from .create_aggregate_by_functions_model import CreateAggregateByFunctionsModel, AggregateGenerationState
from .create_aggregate_class_id_by_drafts_model import CreateAggregateClassIdByDraftsModel, ClassIdGenerationState
from .create_command_actions_by_function_model import CreateCommandActionsByFunctionModel, CommandActionGenerationState
from .create_policy_actions_by_function_model import CreatePolicyActionsByFunctionModel, PolicyActionGenerationState
from .create_gwt_generator_by_function_model import CreateGwtGeneratorByFunctionModel, GWTGenerationState
from .es_value_summary_generator_model import ESValueSummaryGeneratorModel
from .create_ui_components_model import CreateUiComponentsModel, CreateUiComponentsGenerationState
from .create_element_names_by_draft_model import CreateElementNamesByDraftsModel, ElementNamesGenerationState, ExtractedElementNameDetail

class SubgraphsModel(BaseModelWithItem):
    createBoundedContextByFunctionsModel: CreateBoundedContextByFunctionsModel = Field(default_factory=CreateBoundedContextByFunctionsModel)
    createContextMappingModel: CreateContextMappingModel = Field(default_factory=CreateContextMappingModel)
    createDraftByFunctionModel: CreateDraftByFunctionModel = Field(default_factory=CreateDraftByFunctionModel)
    createAggregateByFunctionsModel: CreateAggregateByFunctionsModel = Field(default_factory=CreateAggregateByFunctionsModel)
    createAggregateClassIdByDraftsModel: CreateAggregateClassIdByDraftsModel = Field(default_factory=CreateAggregateClassIdByDraftsModel)
    createElementNamesByDraftsModel: CreateElementNamesByDraftsModel = Field(default_factory=CreateElementNamesByDraftsModel)
    createCommandActionsByFunctionModel: CreateCommandActionsByFunctionModel = Field(default_factory=CreateCommandActionsByFunctionModel)
    createPolicyActionsByFunctionModel: CreatePolicyActionsByFunctionModel = Field(default_factory=CreatePolicyActionsByFunctionModel)
    createGwtGeneratorByFunctionModel: CreateGwtGeneratorByFunctionModel = Field(default_factory=CreateGwtGeneratorByFunctionModel)
    createUiComponentsModel: CreateUiComponentsModel = Field(default_factory=CreateUiComponentsModel)
    esValueSummaryGeneratorModel: ESValueSummaryGeneratorModel = Field(default_factory=ESValueSummaryGeneratorModel)

__all__ = [
    "SubgraphsModel",
    "CreateBoundedContextByFunctionsModel",
    "BoundedContextGenerationState",
    "CreateContextMappingModel",
    "ContextMappingGenerationState",
    "CreateDraftByFunctionModel",
    "DraftGenerationState",
    "CreateAggregateByFunctionsModel",
    "AggregateGenerationState",
    "CreateAggregateClassIdByDraftsModel",
    "ClassIdGenerationState",
    "CreateElementNamesByDraftsModel",
    "ElementNamesGenerationState",
    "ExtractedElementNameDetail",
    "CreateCommandActionsByFunctionModel",
    "CommandActionGenerationState",
    "CreatePolicyActionsByFunctionModel",
    "PolicyActionGenerationState",
    "CreateGwtGeneratorByFunctionModel",
    "GWTGenerationState",
    "CreateUiComponentsModel",
    "CreateUiComponentsGenerationState",
    "ESValueSummaryGeneratorModel"
]
