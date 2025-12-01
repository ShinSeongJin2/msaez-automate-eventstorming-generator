from dataclasses import dataclass

@dataclass(frozen=True)
class ElementType:
    BOUNDED_CONTEXT: str = "org.uengine.modeling.model.BoundedContext"
    AGGREGATE: str = "org.uengine.modeling.model.Aggregate"
    COMMAND: str = "org.uengine.modeling.model.Command"
    EVENT: str = "org.uengine.modeling.model.Event"
    UI: str = "org.uengine.modeling.model.UI"

ELEMENT_TYPES = ElementType()