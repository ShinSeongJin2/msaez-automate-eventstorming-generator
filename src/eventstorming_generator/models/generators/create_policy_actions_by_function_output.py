from pydantic import Field
from typing import List, Optional, Union
from ..base import BaseModelWithItem

Refs = Optional[List[List[List[Union[int, str]]]]]

class ExtractedPolicy(BaseModelWithItem):
    """Represents a policy that connects an event to an event"""
    name: str = Field(description="The name of the policy in English")
    alias: str = Field(description="The alias or display name of the policy")
    reason: str = Field(description="The business reason and purpose for this policy")
    fromEventIds: List[str] = Field(description="The IDs of the source events that triggers this policy")
    toEventIds: List[str] = Field(description="The IDs of the target events that this policy triggers")
    refs: Refs = Field(None, description="Source reference from the functional requirements")

class PolicyResult(BaseModelWithItem):
    """Contains the extracted policies from the analysis"""
    extractedPolicies: List[ExtractedPolicy] = Field(description="List of policies derived from the event storming model")

class CreatePolicyActionsByFunctionOutput(BaseModelWithItem):
    """Output model for policy actions generation based on functional requirements"""
    inference: str = Field(description="The reasoning process and analysis that led to the derived policies")
    result: PolicyResult = Field(description="The result containing all extracted policies")