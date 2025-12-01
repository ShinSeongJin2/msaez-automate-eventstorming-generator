from typing import List
from pydantic import Field
from ..base import BaseModelWithItem
from ...types import LineNumberRange

class ContextMapping(BaseModelWithItem):
    """Mapping between a bounded context and related requirement lines"""
    boundedContextName: str = Field(..., description="Name of the bounded context")
    refs: List[LineNumberRange] = Field(..., description="List of line number ranges [start, end]")

class RequirementMappingGeneratorOutput(BaseModelWithItem):
    """Structured Output Model of the RequirementMappingGenerator"""
    contextMappings: List[ContextMapping] = Field(..., description="Mappings between bounded contexts and requirement lines")