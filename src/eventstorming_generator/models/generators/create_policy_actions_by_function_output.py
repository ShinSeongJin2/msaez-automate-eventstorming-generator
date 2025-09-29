from pydantic import Field
from typing import List
from ..base import BaseModelWithItem

Refs = List[List[List[str]]]

class ExtractedPolicy(BaseModelWithItem):
    """Represents a policy that connects an event to an event"""
    name: str = Field(..., description="The name of the policy in English")
    alias: str = Field(..., description="The alias or display name of the policy")
    reason: str = Field(..., description="The business reason and purpose for this policy")
    fromEventId: str = Field(..., description="The ID of the source event that triggers this policy")
    toEventIds: List[str] = Field(..., description="The IDs of the target events that this policy triggers")
    refs: Refs = Field(..., description="Source reference from the functional requirements")

class CreatePolicyActionsByFunctionOutput(BaseModelWithItem):
    """Output model for policy actions generation based on functional requirements"""
    extractedPolicies: List[ExtractedPolicy] = Field(..., description="List of policies derived from the event storming model")