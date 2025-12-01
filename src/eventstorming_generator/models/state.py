from pydantic import Field

from .base import BaseModelWithItem
from .inputs import InputsModel
from .outputs import OutputsModel
from .subgraphs import SubgraphsModel

class State(BaseModelWithItem):
    inputs: InputsModel = Field(default_factory=InputsModel)
    subgraphs: SubgraphsModel = Field(default_factory=SubgraphsModel)
    outputs: OutputsModel = Field(default_factory=OutputsModel)