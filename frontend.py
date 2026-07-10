import streamlit as st
import requests

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Rohit AI", 
    page_icon="✨", 
    layout="centered",
    initial_sidebar_state="auto" 
)

# --- 2. THEME-AWARE CUSTOM CSS & STUNNING UI ---
st.markdown("""
    <style>
        /* Hide Streamlit default marks */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Fix chat input padding on mobile */
        .stChatInput {padding-bottom: 20px;}
        
        /* Modern styling for the sidebar */
        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(128, 128, 128, 0.2);
            background-color: var(--secondary-background-color);
        }
        
        /* Gradient Text for the Title */
        .gradient-text {
            background: linear-gradient(45deg, #0072ff, #00c6ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 800;
        }
    </style>
""", unsafe_allow_html=True)

# --- 3. STUNNING, MOBILE-RESPONSIVE HEADER ---
st.markdown("""
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 25px; padding-top: 10px;">
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712027.png" width="55" style="flex-shrink: 0; filter: drop-shadow(0px 4px 6px rgba(0,0,0,0.15));">
        <div>
            <h1 style="margin: 0; font-size: 1.9rem;" class="gradient-text">Rohit AI Assistant</h1>
            <p style="margin: 0; font-size: 0.95rem; color: var(--text-color); opacity: 0.75;">⚡ Engineered for excellence, ready to help.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# --- 4. THE SIDEBAR (AUTO-COLLAPSES ON PHONE) ---
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding-bottom: 10px;">
            <h2 style="margin-bottom: 0;">⚙️ Dashboard</h2>
            <p style="color: gray; font-size: 0.85rem; margin-top: 2px;">Rohit AI Enterprise System</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Settings
    model_name = st.selectbox("🧠 AI Brain", ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"])
    allow_search = st.toggle("🌐 Live Web Search", value=True)
    
    with st.expander("🛠️ Advanced Settings"):
        system_prompt = st.text_area(
            "System Prompt", 
            "You are Rohit AI, a highly intelligent, friendly, and concise enterprise AI assistant created by Rohit."
        )
    
    st.divider()
    
    # Clear chat with a nice UI
    if st.button("✨ Start Fresh Chat", use_container_width=True, type="primary"):
        st.session_state.messages = []
        st.rerun()
        
    st.caption("v1.1.0 • Secure Enterprise Cloud")

# --- 5. INITIALIZE HUMAN-LIKE CHAT ---
# Give the AI a friendly first message so the screen isn't empty!
if "messages" not in st.session_state or len(st.session_state.messages) == 0:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi there! 👋 I'm **Rohit AI**. I can search the live web, write code, or just chat. How can I help you today?"}
    ]

# --- 6. DISPLAY CHAT MESSAGES ---
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

# --- 7. CHAT LOGIC & BACKEND CONNECTION ---
if user_input := st.chat_input("Ask Rohit AI anything..."):
    # 1. Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    # 2. Show assistant thinking & call backend
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Processing..."):
            try:
                payload = {
                    "messages": [m["content"] for m in st.session_state.messages if m["role"] == "user"],
                    "system_prompt": system_prompt,
                    "model_name": model_name,
                    "allow_search": allow_search
                }
                
                # ⚠️ CRITICAL: REPLACE THE URL BELOW WITH YOUR RENDER URL!
                # Example: API_URL = "https://langgraph-backend-xyz.onrender.com/chat"
                API_URL = "https://enterprise-langgraph-chatbot.onrender.com/chat"
                
                response = requests.post(API_URL, json=payload)
                
                if response.status_code != 200:
                    st.error(f"🚨 Backend Error: {response.json().get('detail', response.text)}")
                else:
                    ai_reply = response.json()["response"]
                    st.markdown(ai_reply)
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})
                
            except requests.exceptions.ConnectionError:
                st.error("🔌 Connection Error: Your Render backend is asleep or the URL is wrong. (If it is asleep, wait 60s and try again!)")
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
