import streamlit as st
from streamlit_chat import message
from backend.core import run_llm
from dotenv import load_dotenv

def init_page():
    """Initialize the Streamlit page with custom settings"""
    st.set_page_config(
        page_title="LangChain Documentation Helper",
        page_icon="🦜"
    )
    st.header("Chat with LangChain Documentation 🦜")

def init_messages():
    """Initialize the session state messages"""
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    load_dotenv()
    
    # Initialize page and messages
    init_page()
    init_messages()
    
    # Create a chat input
    if user_input := st.chat_input("Ask me anything about LangChain!"):
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.spinner("Thinking..."):
            # Get response from LLM
            result = run_llm(user_input)
            response = result["answer"]
            sources = result["sources"]
            
            # Add response and sources to messages
            st.session_state.messages.append({
                "role": "assistant", 
                "content": response,
                "sources": sources
            })
    
    # Display chat messages in chronological order
    for idx, msg in enumerate(st.session_state.messages):
        is_user = msg["role"] == "user"
        message(
            msg["content"],
            is_user=is_user,
            key=f"msg_{idx}",
            avatar_style="personas" if is_user else None
        )
        
        # Display sources for assistant messages
        if not is_user and "sources" in msg:
            with st.expander("Sources"):
                for source in msg["sources"]:
                    st.write(source)

if __name__ == "__main__":
    main()