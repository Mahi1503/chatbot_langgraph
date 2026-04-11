import streamlit as st
from chatbot_backend_with_sqlite3 import chatbot, retrieve_all_threads
from langchain_core.messages import HumanMessage
import uuid

# utility function to generate unique thread IDs
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(st.session_state["thread_id"])
    st.session_state["message_history"] = []   

def add_thread(thread_id):
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

def load_conversation(thread_id):
    return chatbot.get_state(config={"configurable": {"thread_id": thread_id}}).values["messages"]


# we created key "message_history" in the session state to store the conversation history. 
# This allows us to keep track of all the messages exchanged between the user and the assistant, and display them in the chat interface. Each message is stored as a dictionary with a "role" (either "user" or "assistant") and "content" (the text of the message).

# session state setup

if "message_history" not in st.session_state: # session state is a dictionary that can be used to store data across multiple runs of the app. It is useful for storing data that needs to persist across multiple interactions with the app, such as user input or the state of a chatbot conversation.
    st.session_state["message_history"] = []

if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id() # we generate a unique thread ID for each user session using the generate_thread_id function. This allows us to maintain separate conversations for different users or sessions, ensuring that the conversation history is properly organized and managed.

if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = retrieve_all_threads() # we initialize an empty list in the session state to store chat threads. This allows us to keep track of multiple conversations and their associated thread IDs, enabling users to switch between different conversations or sessions without losing their chat history.

add_thread(st.session_state["thread_id"]) # we add the current thread ID to the list of chat threads in the session state. This ensures that the current conversation is tracked and can be accessed later if needed.   

# Sidebar UI
st.sidebar.title("Langgraph Chatbot")

if st.sidebar.button("New chat"):
    reset_chat()

st.sidebar.header("My conversations")

for thread in st.session_state["chat_threads"][::-1]:
    if st.sidebar.button(str(thread)):
        st.session_state["thread_id"] = thread
        messages = load_conversation(thread)
        
        temp_messages = []

        for message in messages:
            if isinstance(message, HumanMessage):
                role = "user"
            else:
                role = "assistant"
            temp_messages.append({"role": role, "content": message.content})

        st.session_state["message_history"] = temp_messages

# loading conversation history
for message in st.session_state["message_history"]:
    with st.chat_message(message["role"]):
        st.text(message["content"])


user_input = st.chat_input("Type your message here...")


if user_input:
    st.session_state["message_history"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.text(user_input)

    #CONFIG = {"configurable": {"thread_id":st.session_state["thread_id"]}} # This is a configuration dictionary that can be used to customize the behavior of the chatbot. In this case, it includes a "configurable" key with a nested "thread_id" key, which can be used to specify a unique identifier for the chat thread. This allows the chatbot to maintain separate conversations with different users or in different contexts, ensuring that the conversation history is properly organized and managed.
    
    CONFIG = {
        "configurable": {"thread_id":st.session_state["thread_id"]},
        "metadata": {
            "thread_id":st.session_state["thread_id"]
        },
        "run_name":"chat_turn"}
    
    with st.chat_message("assistant"):
        
        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in chatbot.stream(
            {"messages" : [HumanMessage(content=user_input)]},
            config=CONFIG,
            stream_mode="messages"))
        
        
    st.session_state["message_history"].append({"role": "assistant", "content": ai_message})
















   