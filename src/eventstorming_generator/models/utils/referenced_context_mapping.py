from ..base import BaseModelWithItem
from ...types import RequirementIndexMapping
from pydantic import Field

class ReferencedContextMapping(BaseModelWithItem):
    bounded_context_name: str = ""
    requirement_index_mapping: RequirementIndexMapping = Field(default_factory=dict)
    created_requirements: str = ""