from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage,HumanMessage
from typing import TypedDict
from typing_extensions import Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3

from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

import requests
import random

load_dotenv()

llm = ChatOpenAI()

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage],add_messages]


def chat_node(state: ChatState) -> ChatState:
    messages = state['messages']
    response = llm.invoke(messages)
    return {'messages': [response]}

conn = sqlite3.connect(database = 'chatbot.db', check_same_thread=False)

# Checkpointer 
checkpointer = SqliteSaver(conn=conn)


graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None): # we list all checkpoints in the database, and extract the thread IDs from the checkpoint configurations. We use a set to store the thread IDs to ensure that they are unique, and then convert it to a list before returning it we pass None to get all checkpoints we can also extract particular checkpoints.
        all_threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_threads)

