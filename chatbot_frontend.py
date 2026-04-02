import streamlit as st
from chatbot_backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {"configurable": {"thread_id":"thread-1"}} # This is a configuration dictionary that can be used to customize the behavior of the chatbot. In this case, it includes a "configurable" key with a nested "thread_id" key, which can be used to specify a unique identifier for the chat thread. This allows the chatbot to maintain separate conversations with different users or in different contexts, ensuring that the conversation history is properly organized and managed.

# we created key "message_history" in the session state to store the conversation history. 
# This allows us to keep track of all the messages exchanged between the user and the assistant, and display them in the chat interface. Each message is stored as a dictionary with a "role" (either "user" or "assistant") and "content" (the text of the message).

# session state
if "message_history" not in st.session_state: # session state is a dictionary that can be used to store data across multiple runs of the app. It is useful for storing data that needs to persist across multiple interactions with the app, such as user input or the state of a chatbot conversation.
    st.session_state["message_history"] = []


# loading conversation history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])


user_input = st.chat_input("Type your message here...")


if user_input:
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    response = chatbot.invoke({"messages": [HumanMessage(content=user_input)]},config=CONFIG)
    ai_message = response["messages"][-1].content
    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})
    with st.chat_message("assistant"):
        st.text(ai_message) 



















# with st.chat_message("user"):
#     st.text("Hi")

# with st.chat_message("assistant"):
#     st.text("Hello! How can I assist you today?")        