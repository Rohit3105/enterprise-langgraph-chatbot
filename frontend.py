import streamlit as st
import requests

# ─────────────────────────────────────────────────────────────────────────
# 1. Page Configuration (must be the first Streamlit command)
# ─────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Enterprise AI Assistant",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────
# 2. Design tokens + custom CSS
#
#    Root-cause fix: Streamlit auto-switches to a dark palette based on the
#    visitor's OS/browser setting. That's what made replies look "faded" —
#    light gray dark-mode text landing on our white message cards. The
#    .streamlit/config.toml shipped alongside this file locks the app to
#    the light theme so that can't happen. Everything below also sets
#    colors explicitly and with !important on text-bearing elements as a
#    second line of defense.
# ─────────────────────────────────────────────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

        :root {
            --bg: #F3F4F8;
            --surface: #FFFFFF;
            --surface-2: #FAFAFC;
            --border: #E6E8F0;
            --border-strong: #D6D9E4;
            --text-primary: #12131C;
            --text-secondary: #4B4F5C;
            --text-tertiary: #8A8E9C;
            --accent: #423BE6;
            --accent-hover: #352EC9;
            --accent-soft: #EEEDFD;
            --spark: #F5A524;
            --spark-soft: #FEF3E2;
            --success: #17B26A;
            --success-soft: #ECFDF3;
            --danger: #E4483F;
            --danger-soft: #FEF3F2;
            --radius-lg: 18px;
            --radius-md: 12px;
            --radius-sm: 9px;
            --shadow-sm: 0 1px 2px rgba(18, 19, 28, 0.05);
            --shadow-md: 0 6px 20px rgba(18, 19, 28, 0.08);
            --shadow-lg: 0 16px 40px rgba(18, 19, 28, 0.10);
        }

        /* ---------- Base cleanup ---------- */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header[data-testid="stHeader"] {
            background: transparent;
            box-shadow: none;
            height: 2.75rem;
        }
        div[data-testid="stDecoration"] { display: none; }

        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }

        .stApp {
            background:
                radial-gradient(circle at 100% 0%, rgba(66,59,230,0.06), transparent 45%),
                radial-gradient(circle at 0% 20%, rgba(245,165,36,0.05), transparent 40%),
                var(--bg);
            color: var(--text-primary) !important;
        }

        .block-container {
            padding: 1rem 1rem 6rem 1rem;
            max-width: 780px;
        }

        /* Force every text-bearing element back to our own colors,
           overriding whatever theme the browser tries to inject */
        p, span, div, li, label, h1, h2, h3, h4, h5, h6,
        .stMarkdown, .stMarkdown p {
            color: var(--text-primary);
        }

        /* ---------- Header ---------- */
        .brand-header {
            display: flex;
            align-items: center;
            gap: 14px;
            flex-wrap: wrap;
            row-gap: 10px;
            margin-bottom: 2px;
        }
        .brand-mark {
            width: 48px;
            height: 48px;
            flex-shrink: 0;
            border-radius: 13px;
            background: linear-gradient(135deg, var(--accent) 0%, #7A6EF0 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: var(--shadow-md);
            position: relative;
        }
        .brand-mark::after {
            content: "";
            position: absolute;
            inset: 0;
            border-radius: 13px;
            background: linear-gradient(180deg, rgba(255,255,255,0.25), transparent 60%);
        }
        .brand-mark svg { position: relative; z-index: 1; }
        .brand-text { min-width: 0; }
        .brand-title {
            font-size: 1.55rem;
            font-weight: 800;
            color: var(--text-primary) !important;
            letter-spacing: -0.02em;
            line-height: 1.2;
            margin: 0;
        }
        .brand-subtitle {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            font-weight: 600;
            color: var(--text-secondary) !important;
            letter-spacing: 0.02em;
            margin-top: 3px;
        }
        .status-pill {
            margin-left: auto;
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 6px 13px;
            background: var(--success-soft);
            border: 1px solid #CDF2DE;
            border-radius: 999px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            font-weight: 700;
            color: #0A8A50 !important;
            letter-spacing: 0.03em;
            white-space: nowrap;
        }
        .status-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 0 3px rgba(23, 178, 106, 0.18);
        }

        hr {
            border: none;
            border-top: 1px solid var(--border);
            margin: 1.2rem 0 1.4rem 0;
        }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {
            background: var(--surface) !important;
            border-right: 1px solid var(--border-strong);
        }
        section[data-testid="stSidebar"] * {
            color: var(--text-primary) !important;
        }
        section[data-testid="stSidebar"] .block-container {
            padding: 1.8rem 1.15rem 2rem 1.15rem;
        }
        .sb-header {
            display: flex;
            align-items: center;
            gap: 9px;
            margin-bottom: 4px;
        }
        .sb-header-icon {
            width: 30px;
            height: 30px;
            border-radius: 8px;
            background: var(--accent-soft);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 15px;
        }
        .sb-header-title {
            font-size: 1.05rem;
            font-weight: 800;
            color: var(--text-primary) !important;
        }
        .sb-header-desc {
            font-size: 0.78rem;
            color: var(--text-secondary) !important;
            margin-bottom: 1.4rem;
        }

        /* Clearly visible field groups for every sidebar control */
        .field-group {
            background: var(--surface-2);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 12px 14px 14px 14px;
            margin-bottom: 12px;
        }
        .field-label {
            display: flex;
            align-items: center;
            gap: 7px;
            font-size: 0.82rem;
            font-weight: 700;
            color: var(--text-primary) !important;
            margin-bottom: 8px;
        }
        .field-hint {
            font-size: 0.72rem;
            color: var(--text-tertiary) !important;
            margin-top: 6px;
            line-height: 1.4;
        }

        /* Selectbox */
        div[data-baseweb="select"] > div {
            border-radius: var(--radius-sm) !important;
            border-color: var(--border-strong) !important;
            background: var(--surface) !important;
            min-height: 42px !important;
        }
        div[data-baseweb="select"] * {
            color: var(--text-primary) !important;
        }

        /* Text area */
        .stTextArea textarea {
            border-radius: var(--radius-sm) !important;
            border-color: var(--border-strong) !important;
            font-size: 0.85rem !important;
            background: var(--surface) !important;
            color: var(--text-primary) !important;
        }

        /* Toggle */
        div[data-testid="stToggle"] label p {
            font-weight: 600 !important;
            color: var(--text-primary) !important;
        }

        /* Expander */
        div[data-testid="stExpander"] {
            border: 1px solid var(--border-strong) !important;
            border-radius: var(--radius-md) !important;
            background: var(--surface-2) !important;
        }
        div[data-testid="stExpander"] summary {
            font-size: 0.85rem;
            font-weight: 700;
            color: var(--text-primary) !important;
        }

        /* Buttons */
        .stButton > button {
            border-radius: var(--radius-sm) !important;
            font-weight: 700 !important;
            font-size: 0.85rem !important;
            border: 1.5px solid var(--danger) !important;
            background: var(--danger-soft) !important;
            color: var(--danger) !important;
            transition: all 0.15s ease;
            padding: 0.55rem 1rem !important;
        }
        .stButton > button:hover {
            background: var(--danger) !important;
            color: #FFFFFF !important;
        }
        .stButton > button p { color: inherit !important; }

        .sidebar-footer {
            margin-top: 1.6rem;
            padding-top: 14px;
            border-top: 1px solid var(--border);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            color: var(--text-tertiary) !important;
            letter-spacing: 0.02em;
            line-height: 1.6;
        }

        /* Model badge */
        .model-badge {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.7rem;
            font-weight: 700;
            color: var(--accent) !important;
            background: var(--accent-soft);
            padding: 4px 10px;
            border-radius: 999px;
            margin-top: 8px;
            max-width: 100%;
            box-sizing: border-box;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        /* ---------- Chat messages ---------- */
        div[data-testid="stChatMessage"] {
            background: var(--surface) !important;
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 8px 14px 12px 14px;
            margin-bottom: 14px;
            box-shadow: var(--shadow-sm);
        }
        div[data-testid="stChatMessage"] p,
        div[data-testid="stChatMessage"] li,
        div[data-testid="stChatMessage"] span,
        div[data-testid="stChatMessage"] div {
            color: var(--text-primary) !important;
            font-size: 0.95rem;
            line-height: 1.6;
        }
        div[data-testid="stChatMessage"] code {
            background: var(--surface-2) !important;
            color: #C0255C !important;
            border-radius: 5px;
            padding: 2px 5px;
        }
        div[data-testid="stChatMessage"] pre {
            background: #12131C !important;
            border-radius: var(--radius-sm) !important;
        }
        div[data-testid="stChatMessage"] pre code {
            background: transparent !important;
            color: #E6E8F0 !important;
        }

        .msg-role {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.66rem;
            font-weight: 700;
            letter-spacing: 0.07em;
            text-transform: uppercase;
            color: var(--text-tertiary) !important;
            margin-bottom: 3px;
        }

        /* ---------- Empty state ---------- */
        .empty-state {
            text-align: center;
            padding: 48px 20px;
            color: var(--text-secondary) !important;
        }
        .empty-state-icon {
            width: 56px;
            height: 56px;
            margin: 0 auto 16px auto;
            border-radius: 14px;
            background: linear-gradient(135deg, var(--accent) 0%, #7A6EF0 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: var(--shadow-md);
        }
        .empty-state-title {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-primary) !important;
            margin-bottom: 6px;
        }
        .empty-state-desc {
            font-size: 0.85rem;
            color: var(--text-tertiary) !important;
            max-width: 320px;
            margin: 0 auto;
            line-height: 1.5;
        }

        /* ---------- Chat input ---------- */
        .stChatInput { padding-bottom: 18px; }
        div[data-testid="stChatInput"] {
            border-radius: var(--radius-lg) !important;
            border: 1.5px solid var(--border-strong) !important;
            background: var(--surface) !important;
            box-shadow: var(--shadow-lg);
        }
        div[data-testid="stChatInput"] textarea {
            color: var(--text-primary) !important;
        }
        div[data-testid="stChatInput"] textarea::placeholder {
            color: var(--text-tertiary) !important;
        }

        /* ---------- Alerts ---------- */
        div[data-testid="stAlert"] {
            border-radius: var(--radius-md) !important;
            font-size: 0.88rem;
        }
        div[data-testid="stAlert"] p {
            color: inherit !important;
        }

        /* ---------- Spinner text ---------- */
        div[data-testid="stSpinner"] p {
            color: var(--text-secondary) !important;
            font-size: 0.85rem;
            font-weight: 500;
        }

        /* ───────────────────────────────────────────────────────────
           MOBILE / NARROW SCREEN LAYOUT (≤640px)
        ─────────────────────────────────────────────────────────── */
        @media (max-width: 640px) {

            .block-container {
                padding: 3.4rem 0.7rem 6.5rem 0.7rem !important;
            }

            .brand-mark { width: 40px; height: 40px; border-radius: 11px; }
            .brand-mark svg { width: 19px; height: 19px; }
            .brand-title { font-size: 1.2rem; }
            .brand-subtitle { font-size: 0.6rem; line-height: 1.4; white-space: normal; }

            .status-pill {
                margin-left: 0;
                width: 100%;
                justify-content: center;
                order: 3;
            }

            hr { margin: 0.9rem 0 1rem 0; }

            div[data-testid="stChatMessage"] {
                padding: 6px 10px 10px 10px;
                margin-bottom: 10px;
                border-radius: 14px;
            }
            div[data-testid="stChatMessage"] p,
            div[data-testid="stChatMessage"] li {
                font-size: 0.92rem;
            }

            div[data-testid="stChatInput"] { border-radius: 16px !important; }

            section[data-testid="stSidebar"] .block-container {
                padding: 1.4rem 1rem 2rem 1rem;
            }

            .empty-state { padding: 32px 12px; }
        }
    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────
# 3. Header — custom brand mark (inline SVG, no external image dependency)
# ─────────────────────────────────────────────────────────────────────────
st.markdown("""
    <div class="brand-header">
        <div class="brand-mark">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M13 2L4 14H11L10 22L20 9H13L13 2Z" fill="white"/>
            </svg>
        </div>
        <div class="brand-text">
            <p class="brand-title">Enterprise AI Assistant</p>
            <p class="brand-subtitle">GROQ LPUs · LANGGRAPH · FASTAPI</p>
        </div>
        <div class="status-pill">
            <span class="status-dot"></span>
            SESSION ACTIVE
        </div>
    </div>
    <hr>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────
# 4. Sidebar — Control Panel (every control gets its own clearly bordered,
#    clearly labeled card so nothing reads as "missing")
# ─────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div class="sb-header">
            <div class="sb-header-icon">⚙️</div>
            <div class="sb-header-title">Control Panel</div>
        </div>
        <p class="sb-header-desc">Configure the model and behavior for this session.</p>
    """, unsafe_allow_html=True)

    st.markdown('<div class="field-group">', unsafe_allow_html=True)
    st.markdown('<p class="field-label">🧠 &nbsp;Brain Engine</p>', unsafe_allow_html=True)
    model_name = st.selectbox(
        "Brain Engine",
        ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
        label_visibility="collapsed",
    )
    st.markdown(f'<span class="model-badge">● {model_name}</span>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="field-group">', unsafe_allow_html=True)
    st.markdown('<p class="field-label">🌐 &nbsp;Live Web Search</p>', unsafe_allow_html=True)
    allow_search = st.toggle("Enable Live Web Search", value=True, label_visibility="collapsed")
    st.markdown('<p class="field-hint">When on, the assistant can pull in current information from the web.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="field-group">', unsafe_allow_html=True)
    st.markdown('<p class="field-label">🛠️ &nbsp;Advanced Settings</p>', unsafe_allow_html=True)
    with st.expander("System Prompt"):
        system_prompt = st.text_area(
            "System Prompt",
            "You are a highly intelligent, concise AI assistant.",
            label_visibility="collapsed",
            height=100,
        )
    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🗑️  Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.markdown("""
        <div class="sidebar-footer">
            v1.0.0 · FastAPI backend<br>127.0.0.1:8000
        </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────
# 5. Initialize Chat History
# ─────────────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ─────────────────────────────────────────────────────────────────────────
# 6. Render Chat History (or a welcoming empty state if there's nothing yet)
# ─────────────────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
        <div class="empty-state">
            <div class="empty-state-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M13 2L4 14H11L10 22L20 9H13L13 2Z" fill="white"/>
                </svg>
            </div>
            <p class="empty-state-title">Start a conversation</p>
            <p class="empty-state-desc">Ask a question, paste something to analyze, or describe a task — the assistant is ready.</p>
        </div>
    """, unsafe_allow_html=True)

for msg in st.session_state.messages:
    avatar = ":material/person:" if msg["role"] == "user" else ":material/bolt:"
    role_label = "You" if msg["role"] == "user" else "Assistant"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(f'<div class="msg-role">{role_label}</div>', unsafe_allow_html=True)
        st.markdown(msg["content"])

# ─────────────────────────────────────────────────────────────────────────
# 7. Chat Logic
# ─────────────────────────────────────────────────────────────────────────
if user_input := st.chat_input("Type your message here..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar=":material/person:"):
        st.markdown('<div class="msg-role">You</div>', unsafe_allow_html=True)
        st.markdown(user_input)

    # Communicate with Backend
    with st.chat_message("assistant", avatar=":material/bolt:"):
        st.markdown('<div class="msg-role">Assistant</div>', unsafe_allow_html=True)
        with st.spinner("Processing at lightning speed..."):
            try:
                payload = {
                    "messages": [m["content"] for m in st.session_state.messages if m["role"] == "user"],
                    "system_prompt": system_prompt,
                    "model_name": model_name,
                    "allow_search": allow_search
                }

                response = requests.post("https://enterprise-langgraph-chatbot.onrender.com/chat", json=payload)

                if response.status_code != 200:
                    st.error(f"🚨 Backend Error: {response.json().get('detail', response.text)}")
                else:
                    ai_reply = response.json()["response"]
                    st.markdown(ai_reply)
                    st.session_state.messages.append({"role": "assistant", "content": ai_reply})

            except requests.exceptions.ConnectionError:
                st.error("🔌 Connection Error: Make sure your FastAPI backend is running!")
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
