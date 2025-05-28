from pydantic import Field
from typing import List
from ..base import BaseModelWithItem

class ExtractedPolicy(BaseModelWithItem):
    """Represents a policy that connects an event to a command"""
    name: str = Field(description="The name of the policy in English")
    alias: str = Field(description="The alias or display name of the policy")
    reason: str = Field(description="The business reason and purpose for this policy")
    fromEventId: str = Field(description="The ID of the source event that triggers this policy")
    toCommandId: str = Field(description="The ID of the target command that this policy executes")

class PolicyResult(BaseModelWithItem):
    """Contains the extracted policies from the analysis"""
    extractedPolicies: List[ExtractedPolicy] = Field(description="List of policies derived from the event storming model")

class CreatePolicyActionsByFunctionOutput(BaseModelWithItem):
    """Output model for policy actions generation based on functional requirements"""
    inference: str = Field(description="The reasoning process and analysis that led to the derived policies")
    result: PolicyResult = Field(description="The result containing all extracted policies")