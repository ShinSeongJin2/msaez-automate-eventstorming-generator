from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from typing import Annotated
from pydantic import BaseModel, Field
import os

class State(BaseModel):
    messages: Annotated[list, add_messages] = Field(default_factory=list)

def chatbot(state: State):
    llm = init_chat_model(os.environ["AI_MODEL"])
    return {"messages": [llm.invoke(state.messages)]}

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile()