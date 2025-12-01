from dataclasses import dataclass

@dataclass(frozen=True)
class RequestType:
    FROM_DRAFT: str = "fromDraft"
    FROM_REQUIREMENTS: str = "fromRequirements"

REQUEST_TYPES = RequestType()