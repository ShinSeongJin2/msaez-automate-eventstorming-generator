from langgraph.graph import StateGraph, START, END

from eventstorming_generator.models import InputsModel, OutputsModel, BaseModelWithItem

class State(BaseModelWithItem):
    inputs: InputsModel = InputsModel()
    outputs: OutputsModel = OutputsModel()

def chatbot(state: State):
    print(state)
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()