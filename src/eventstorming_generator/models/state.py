

from .base import BaseModelWithItem
from .inputs import InputsModel
from .outputs import OutputsModel
from .subgraphs import SubgraphsModel

class State(BaseModelWithItem):
    inputs: InputsModel = InputsModel()
    subgraphs: SubgraphsModel = SubgraphsModel()
    outputs: OutputsModel = OutputsModel()