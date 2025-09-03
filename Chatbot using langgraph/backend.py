# backend.py

from langgraph.graph import StateGraph, START, END, add_messages
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import TypedDict, Annotated
from langgraph.graph.message import BaseMessage
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.checkpoint.memory import InMemorySaver
import os

os.environ['GOOGLE_API_KEY'] = 'AIzaSyB8du31T_IfbT5L61IjOr8T2HpgaINNk7I'

# LLM
model = ChatGoogleGenerativeAI(
    model='gemini-1.5-flash',
    temperature=0.2,
    google_api_key=os.environ['GOOGLE_API_KEY']
)

# State
class ChatState(TypedDict):
    message: Annotated[list[BaseMessage], add_messages]

# Function
def chat(state: ChatState):
    messages = state['message']
    response = model.invoke(messages).content
    return {"message": messages + [AIMessage(content=response)]}

# Graph
checkpointer = InMemorySaver()
graph = StateGraph(ChatState)
graph.add_node("message", chat)
graph.add_edge(START, "message")
graph.add_edge("message", END)

chatbot = graph.compile(checkpointer=checkpointer)

# Terminal mode (only runs if you call python backend.py directly)
if __name__ == "__main__":
    thread_id = "1"
    while True:
        user_input = input("Ask me anything.... ")
        if user_input.strip().lower() in ["quit", "exit", "byee"]:
            print("AI: Goodbyee")
            break

        config = {"configurable": {"thread_id": thread_id}}
        response = chatbot.invoke({"message": [HumanMessage(content=user_input)]}, config=config)
        print("AI:", response["message"][-1].content)
