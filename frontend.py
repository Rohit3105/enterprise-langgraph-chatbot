import streamlit as st
import requests

st.set_page_config(page_title="Enterprise AI Chatbot", layout="centered")
st.title("🤖 Dynamic LangGraph Chatbot")

# Sidebar settings for your presentation
with st.sidebar:
    st.header("Agent Settings")
    # Using Groq's lightning-fast free models
    model_name = st.selectbox("Select Model", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
    allow_search = st.toggle("Enable Web Search (Tavily)", value=True)
    system_prompt = st.text_area("System Prompt", "You are a highly intelligent, concise AI assistant.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                payload = {
                    "messages": [m["content"] for m in st.session_state.messages if m["role"] == "user"],
                    "system_prompt": system_prompt,
                    "model_name": model_name,
                    "allow_search": allow_search
                }
                
                response = requests.post("http://127.0.0.1:8000/chat", json=payload)
                
                # If the backend crashes, print the EXACT reason to the screen
                if response.status_code != 200:
                    st.error(f"🚨 Real Error: {response.json().get('detail', response.text)}")
                else:
                    ai_reply = response.json()["response"]
                    st.markdown(ai_reply)
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                
            except requests.exceptions.ConnectionError:
                st.error("Backend Error: Is the FastAPI server running on your laptop?")
            except Exception as e:
                st.error(f"Error: {e}")