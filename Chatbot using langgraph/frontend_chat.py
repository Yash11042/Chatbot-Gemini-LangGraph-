import streamlit as st
from backend import chatbot  # Import chatbot from your backend file
from langchain_core.messages import HumanMessage

# Keep conversation history in Streamlit's session state
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

# Title
st.title("💬 AI Chatbot (LangGraph + Gemini)")

# Display chat history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Save user message
    st.session_state['message_history'].append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare config (thread_id ensures conversation continuity)
    config = {"configurable": {"thread_id": "1"}}

    # Get AI response from backend chatbot
    response = chatbot.invoke({"message": [HumanMessage(content=user_input)]}, config=config)
    ai_message = response["message"][-1].content

    # Save AI message
    st.session_state['message_history'].append(
        {"role": "AI", "content": ai_message}
    )
    with st.chat_message("AI"):
        st.markdown(ai_message)
