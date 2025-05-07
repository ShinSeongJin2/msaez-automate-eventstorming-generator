from langgraph.graph import StateGraph, START, END
from typing import Optional, Dict
from pydantic import BaseModel

from eventstorming_generator.models import SelectedDraftOptionItem, UserInfoModel, InformationModel

class State(BaseModel):
    selectedDraftOptions: Optional[Dict[str, SelectedDraftOptionItem]] = None
    userInfo: Optional[UserInfoModel] = None
    information: Optional[InformationModel] = None

def chatbot(state: State):
    print(state)
    return state

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()