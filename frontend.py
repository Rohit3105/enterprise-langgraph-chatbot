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
#    Palette: cool neutral surface, deep indigo accent, amber "spark" accent
#    Type: Inter (UI/body) + JetBrains Mono (labels, badges, technical bits)
# ─────────────────────────────────────────────────────────────────────────
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap');

        :root {
            --bg: #F4F5F8;
            --surface: #FFFFFF;
            --border: #E5E7EE;
            --text-primary: #12131C;
            --text-secondary: #667085;
            --text-tertiary: #98A2B3;
            --accent: #423BE6;
            --accent-hover: #352EC9;
            --accent-soft: #EEEDFD;
            --spark: #F5A524;
            --success: #17B26A;
            --danger: #E4483F;
            --radius-lg: 16px;
            --radius-md: 12px;
            --radius-sm: 8px;
            --shadow-sm: 0 1px 2px rgba(18, 19, 28, 0.04);
            --shadow-md: 0 8px 24px rgba(18, 19, 28, 0.06);
        }

        /* ---------- Base cleanup ---------- */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        /* Keep the header element itself (it carries the sidebar toggle arrow
           on mobile) but make it blend in instead of disappearing. */
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
            background: var(--bg);
        }

        .block-container {
            padding-top: 1rem;
            max-width: 780px;
        }

        /* ---------- Header ---------- */
        .brand-header {
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 4px;
        }
        .brand-mark {
            width: 46px;
            height: 46px;
            flex-shrink: 0;
            border-radius: 12px;
            background: linear-gradient(135deg, var(--accent) 0%, #6B63F5 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: var(--shadow-md);
        }
        .brand-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
            letter-spacing: -0.02em;
            line-height: 1.2;
            margin: 0;
        }
        .brand-subtitle {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.72rem;
            font-weight: 500;
            color: var(--text-secondary);
            letter-spacing: 0.02em;
            margin-top: 2px;
        }
        .status-pill {
            margin-left: auto;
            display: flex;
            align-items: center;
            gap: 6px;
            padding: 5px 12px;
            background: #ECFDF3;
            border: 1px solid #D7F5E3;
            border-radius: 999px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            font-weight: 600;
            color: var(--success);
            letter-spacing: 0.02em;
            white-space: nowrap;
        }
        .status-dot {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--success);
            box-shadow: 0 0 0 3px rgba(23, 178, 106, 0.15);
        }

        hr {
            border: none;
            border-top: 1px solid var(--border);
            margin: 1.4rem 0 1.6rem 0;
        }

        /* ---------- Sidebar ---------- */
        section[data-testid="stSidebar"] {
            background: var(--surface);
            border-right: 1px solid var(--border);
        }
        section[data-testid="stSidebar"] .block-container {
            padding-top: 2rem;
        }
        .sidebar-eyebrow {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            font-weight: 600;
            color: var(--text-tertiary);
            letter-spacing: 0.08em;
            text-transform: uppercase;
            margin: 18px 0 6px 0;
        }
        .sidebar-eyebrow:first-of-type { margin-top: 0; }

        section[data-testid="stSidebar"] h2 {
            font-size: 1.05rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 1.2rem;
        }

        /* Selectbox / inputs */
        div[data-baseweb="select"] > div {
            border-radius: var(--radius-sm) !important;
            border-color: var(--border) !important;
            background: var(--bg) !important;
        }
        .stTextArea textarea {
            border-radius: var(--radius-sm) !important;
            border-color: var(--border) !important;
            font-size: 0.85rem !important;
            background: var(--bg) !important;
        }

        /* Toggle */
        div[data-testid="stToggle"] label { font-weight: 500; }

        /* Expander */
        div[data-testid="stExpander"] {
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            background: var(--bg) !important;
        }
        div[data-testid="stExpander"] summary {
            font-size: 0.85rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        /* Buttons */
        .stButton > button {
            border-radius: var(--radius-sm) !important;
            font-weight: 600 !important;
            font-size: 0.85rem !important;
            border: 1px solid var(--border) !important;
            background: var(--surface) !important;
            color: var(--text-secondary) !important;
            transition: all 0.15s ease;
        }
        .stButton > button:hover {
            border-color: var(--danger) !important;
            color: var(--danger) !important;
            background: #FEF3F2 !important;
        }

        .sidebar-footer {
            margin-top: 2.2rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            color: var(--text-tertiary);
            letter-spacing: 0.02em;
        }

        /* ---------- Chat messages ---------- */
        div[data-testid="stChatMessage"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 4px 8px;
            margin-bottom: 12px;
            box-shadow: var(--shadow-sm);
        }

        .msg-role {
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            font-weight: 600;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            color: var(--text-tertiary);
            margin-bottom: 2px;
        }

        /* ---------- Chat input ---------- */
        .stChatInput {padding-bottom: 20px;}
        div[data-testid="stChatInput"] {
            border-radius: var(--radius-lg) !important;
            border: 1px solid var(--border) !important;
            background: var(--surface) !important;
            box-shadow: var(--shadow-md);
        }

        /* ---------- Alerts ---------- */
        div[data-testid="stAlert"] {
            border-radius: var(--radius-md) !important;
            font-size: 0.88rem;
        }

        /* ---------- Model badge in sidebar ---------- */
        .model-badge {
            display: inline-block;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.68rem;
            font-weight: 600;
            color: var(--accent);
            background: var(--accent-soft);
            padding: 3px 9px;
            border-radius: 999px;
            margin-top: 6px;
            max-width: 100%;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        /* ───────────────────────────────────────────────────────────
           MOBILE / NARROW SCREEN LAYOUT
           Everything below only kicks in under 640px so desktop is
           untouched.
        ─────────────────────────────────────────────────────────── */
        @media (max-width: 640px) {

            .block-container {
                padding: 3.2rem 0.85rem 6rem 0.85rem !important;
            }

            /* Header: let the pill drop under the title instead of
               squeezing everything into one row */
            .brand-header {
                flex-wrap: wrap;
                row-gap: 8px;
                margin-bottom: 0;
            }
            .brand-mark {
                width: 38px;
                height: 38px;
                border-radius: 10px;
            }
            .brand-mark svg {
                width: 18px;
                height: 18px;
            }
            .brand-title {
                font-size: 1.15rem;
            }
            .brand-subtitle {
                font-size: 0.6rem;
                line-height: 1.4;
                white-space: normal;
            }
            .status-pill {
                margin-left: 0;
                order: 3;
                width: 100%;
                justify-content: center;
                margin-top: 4px;
            }

            hr {
                margin: 1rem 0 1.1rem 0;
            }

            /* Chat messages: tighter padding, full width use */
            div[data-testid="stChatMessage"] {
                padding: 3px 6px;
                margin-bottom: 9px;
                border-radius: 14px;
            }
            .msg-role {
                font-size: 0.62rem;
            }

            /* Chat input: sit flush with screen edges, no floating card look */
            div[data-testid="stChatInput"] {
                border-radius: 14px !important;
            }
            .stChatInput {
                padding-bottom: 10px;
            }

            /* Sidebar: full-width comfortable padding when opened as a drawer */
            section[data-testid="stSidebar"] .block-container {
                padding: 1.5rem 1rem !important;
            }

            .model-badge {
                width: 100%;
                box-sizing: border-box;
            }
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
        <div>
            <p class="brand-title">Enterprise AI Assistant</p>
            <p class="brand-subtitle">POWERED BY GROQ LPUs · LANGGRAPH · FASTAPI</p>
        </div>
        <div class="status-pill">
            <span class="status-dot"></span>
            SESSION ACTIVE
        </div>
    </div>
    <hr>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────
# 4. Sidebar — Control Panel
# ─────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Control Panel")

    st.markdown('<p class="sidebar-eyebrow">Brain Engine</p>', unsafe_allow_html=True)
    model_name = st.selectbox(
        "Brain Engine",
        ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"],
        label_visibility="collapsed",
    )
    st.markdown(f'<span class="model-badge">● {model_name}</span>', unsafe_allow_html=True)

    st.markdown('<p class="sidebar-eyebrow">Live Data</p>', unsafe_allow_html=True)
    allow_search = st.toggle("Enable Live Web Search", value=True)

    st.markdown('<p class="sidebar-eyebrow">Configuration</p>', unsafe_allow_html=True)
    with st.expander("🛠️ Advanced Settings"):
        system_prompt = st.text_area(
            "System Prompt",
            "You are a highly intelligent, concise AI assistant.",
            label_visibility="collapsed",
            height=100,
        )

    st.markdown("<br>", unsafe_allow_html=True)
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
# 6. Render Chat History
# ─────────────────────────────────────────────────────────────────────────
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

                response = requests.post("http://127.0.0.1:8000/chat", json=payload)

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
