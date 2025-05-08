from langgraph.graph import StateGraph, START, END
from typing import Any
from pydantic import BaseModel

class State(BaseModel):
    selectedDraftOptions: Any = None
    userInfo: Any = None
    information: Any = None
    createEsValue: Any = None

def chatbot(state: State):
    print(state)
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()