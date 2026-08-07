import streamlit as st
import os

# Setup page config (Must be the first Streamlit command)
st.set_page_config(
    page_title="AI English Evaluator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    :root {
        --neon-cyan: #00f5ff;
        --neon-purple: #a855f7;
        --neon-pink: #ec4899;
        --neon-blue: #3b82f6;
        --glass-bg: rgba(17, 25, 40, 0.55);
        --glass-border: rgba(255, 255, 255, 0.08);
        --glass-border-hover: rgba(0, 245, 255, 0.4);
        --text-primary: #e6f1ff;
        --text-secondary: #94a3b8;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: var(--text-primary);
    }

    /* ===== Animated gradient background ===== */
    .stApp {
        background-color: #060913;
        background-image:
            radial-gradient(circle at 10% 20%, rgba(0, 245, 255, 0.10), transparent 35%),
            radial-gradient(circle at 90% 10%, rgba(168, 85, 247, 0.12), transparent 35%),
            radial-gradient(circle at 50% 90%, rgba(236, 72, 153, 0.08), transparent 40%),
            radial-gradient(circle at 80% 80%, rgba(59, 130, 246, 0.08), transparent 35%);
        background-attachment: fixed;
        background-size: 200% 200%;
        animation: gradientShift 18s ease infinite;
    }

    @keyframes gradientShift {
        0%   { background-position: 0% 0%; }
        50%  { background-position: 100% 100%; }
        100% { background-position: 0% 0%; }
    }

    /* Subtle noise/grid overlay for premium texture */
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
        background-size: 48px 48px;
        pointer-events: none;
        z-index: 0;
    }

    /* ===== Sidebar — frosted glass ===== */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(10, 14, 26, 0.85), rgba(10, 14, 26, 0.65)) !important;
        border-right: 1px solid var(--glass-border);
        backdrop-filter: blur(18px) saturate(140%);
        -webkit-backdrop-filter: blur(18px) saturate(140%);
        box-shadow: 4px 0 30px rgba(0, 0, 0, 0.4);
    }

    [data-testid="stSidebar"] * {
        transition: color 0.25s ease;
    }

    /* Sidebar nav links */
    [data-testid="stSidebarNav"] a, section[data-testid="stSidebar"] a {
        border-radius: 8px !important;
        transition: all 0.25s ease !important;
    }
    [data-testid="stSidebarNav"] a:hover, section[data-testid="stSidebar"] a:hover {
        background: rgba(0, 245, 255, 0.08) !important;
        box-shadow: inset 0 0 0 1px rgba(0, 245, 255, 0.25);
        transform: translateX(3px);
    }

    /* ===== Headers — neon glow gradient text ===== */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', sans-serif;
        font-weight: 600;
        letter-spacing: 0.5px;
        background: linear-gradient(90deg, var(--neon-cyan) 0%, var(--neon-purple) 55%, var(--neon-pink) 100%);
        -webkit-background-clip: text;
        background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0 0 12px rgba(0, 245, 255, 0.25));
    }

    /* ===== Buttons — neon gradient with glow hover ===== */
    .stButton>button {
        position: relative;
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9), rgba(30, 41, 59, 0.9));
        color: var(--neon-cyan);
        border-radius: 10px;
        border: 1px solid rgba(0, 245, 255, 0.35);
        padding: 0.6rem 1.3rem;
        font-weight: 600;
        font-family: 'Orbitron', sans-serif;
        font-size: 0.85rem;
        letter-spacing: 0.5px;
        transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 0 0 rgba(0, 245, 255, 0);
    }

    .stButton>button:hover {
        color: #ffffff;
        border-color: var(--neon-cyan);
        transform: translateY(-3px) scale(1.02);
        box-shadow:
            0 8px 24px rgba(0, 245, 255, 0.25),
            0 0 20px rgba(168, 85, 247, 0.25);
        background: linear-gradient(135deg, rgba(30, 41, 59, 0.95), rgba(51, 65, 85, 0.95));
    }

    .stButton>button:active {
        transform: translateY(-1px) scale(0.99);
    }

    /* Primary buttons get a full neon gradient fill */
    .stButton>button[kind="primary"] {
        background: linear-gradient(90deg, var(--neon-blue), var(--neon-purple), var(--neon-pink));
        color: #ffffff;
        border: none;
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.35);
    }
    .stButton>button[kind="primary"]:hover {
        box-shadow: 0 8px 30px rgba(168, 85, 247, 0.55);
        filter: brightness(1.1);
    }

    /* ===== Text areas & inputs — glass fields ===== */
    .stTextArea>div>div>textarea,
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stSelectbox>div>div {
        border-radius: 10px !important;
        border: 1px solid var(--glass-border) !important;
        background-color: rgba(15, 23, 42, 0.5) !important;
        color: var(--text-primary) !important;
        padding: 0.8rem !important;
        font-family: 'Inter', sans-serif;
        backdrop-filter: blur(8px);
        transition: all 0.3s ease;
    }

    .stTextArea>div>div>textarea:focus,
    .stTextInput>div>div>input:focus {
        border-color: var(--neon-cyan) !important;
        box-shadow: 0 0 0 3px rgba(0, 245, 255, 0.15), 0 0 20px rgba(0, 245, 255, 0.1) !important;
    }

    /* ===== Glass cards / containers ===== */
    div[data-testid="stVerticalBlockBorderWrapper"],
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        background: var(--glass-bg);
        padding: 1.75rem;
        border-radius: 16px;
        box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.45),
            inset 0 1px 0 rgba(255, 255, 255, 0.04);
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(14px) saturate(150%);
        -webkit-backdrop-filter: blur(14px) saturate(150%);
        transition: border-color 0.35s ease, box-shadow 0.35s ease, transform 0.25s ease;
    }

    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: var(--glass-border-hover);
        box-shadow:
            0 12px 40px rgba(0, 0, 0, 0.5),
            0 0 24px rgba(0, 245, 255, 0.08);
    }

    /* ===== Metrics — glowing stat cards ===== */
    [data-testid="stMetric"] {
        background: rgba(15, 23, 42, 0.45);
        border: 1px solid var(--glass-border);
        border-radius: 14px;
        padding: 1.1rem 1.3rem;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    [data-testid="stMetric"]:hover {
        border-color: rgba(168, 85, 247, 0.4);
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.15);
        transform: translateY(-2px);
    }
    [data-testid="stMetricValue"] {
        color: var(--neon-cyan) !important;
        font-family: 'Orbitron', sans-serif;
        text-shadow: 0 0 14px rgba(0, 245, 255, 0.35);
    }
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        letter-spacing: 0.3px;
    }

    /* ===== Progress bars — neon gradient fill ===== */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--neon-cyan), var(--neon-purple), var(--neon-pink)) !important;
        border-radius: 8px;
        box-shadow: 0 0 12px rgba(0, 245, 255, 0.4);
    }
    .stProgress > div > div > div {
        background-color: rgba(255, 255, 255, 0.06) !important;
        border-radius: 8px;
    }

    /* ===== Tabs — glass pill style ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background: rgba(15, 23, 42, 0.4);
        padding: 6px;
        border-radius: 12px;
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(10px);
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        color: var(--text-secondary);
        font-family: 'Orbitron', sans-serif;
        font-size: 0.8rem;
        transition: all 0.25s ease;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, rgba(0, 245, 255, 0.15), rgba(168, 85, 247, 0.15));
        color: var(--neon-cyan) !important;
        box-shadow: inset 0 0 0 1px rgba(0, 245, 255, 0.3);
    }

    /* ===== Markdown / body text ===== */
    .stMarkdown, p, li {
        color: var(--text-secondary);
        line-height: 1.6;
    }

    /* ===== Alerts — glass with neon accent ===== */
    .stAlert {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(0, 245, 255, 0.25) !important;
        border-radius: 12px !important;
        color: var(--text-primary) !important;
        backdrop-filter: blur(10px);
    }

    /* ===== Dataframe / tables ===== */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid var(--glass-border);
    }

    /* ===== Expander — glass panel ===== */
    .streamlit-expanderHeader, [data-testid="stExpander"] {
        background: rgba(15, 23, 42, 0.4) !important;
        border-radius: 10px !important;
        border: 1px solid var(--glass-border) !important;
        backdrop-filter: blur(8px);
    }

    /* ===== Scrollbar ===== */
    ::-webkit-scrollbar { width: 10px; height: 10px; }
    ::-webkit-scrollbar-track { background: rgba(15, 23, 42, 0.4); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, var(--neon-cyan), var(--neon-purple));
        border-radius: 6px;
    }

    /* ===== Divider glow ===== */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(0, 245, 255, 0.4), transparent);
        margin: 1.5rem 0;
    }

    /* Ensure content sits above the grid overlay */
    section.main > div { position: relative; z-index: 1; }


    /* ===== Custom sidebar model/API cards ===== */
    .sidebar-model-title {
        margin: 24px 0 12px 4px;
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 1.5px;
    }
    .sidebar-model-card {
        padding: 18px;
        border-radius: 18px;
        border: 1px solid rgba(148,163,184,.35);
        background: linear-gradient(145deg, rgba(15,23,42,.85), rgba(8,15,30,.75));
        box-shadow: 0 10px 30px rgba(0,0,0,.25), inset 0 1px 0 rgba(255,255,255,.03);
    }
    .sidebar-model-heading {
        display: flex; align-items: center; gap: 10px; margin-bottom: 26px;
        color: #00f5ff; font-size: 1.05rem; font-weight: 700;
    }
    .model-icon { font-size: 1.1rem; }
    .model-item { padding: 4px 0; }
    .model-name { color: #e6f1ff; font-size: .95rem; font-weight: 700; margin-bottom: 8px; }
    .model-desc { color: #94a3b8; font-size: .82rem; line-height: 1.5; }
    .model-link { color: #3b82f6; text-decoration: underline; }
    .model-divider { height: 1px; margin: 18px 0; background: rgba(148,163,184,.2); }
    .api-title { margin-top: 28px; }
    .sidebar-api-card {
        padding: 12px 16px; border-radius: 16px; border: 1px solid rgba(148,163,184,.25);
        background: rgba(15,23,42,.55);
    }
    .api-row { display:flex; justify-content:space-between; align-items:center; padding: 8px 0; color:#cbd5e1; font-size:.85rem; }
    .api-status { width: 28px; height: 28px; border-radius:50%; display:flex; align-items:center; justify-content:center; font-weight:800; }
    .api-status.ok { color:#22c55e; border:1px solid #22c55e; }
    .api-status.off { color:#f59e0b; border:1px solid #f59e0b; }
    .sidebar-ready {
        display:flex; gap:12px; align-items:flex-start; margin-top:14px; padding:14px;
        border-radius:14px; border:1px solid rgba(59,130,246,.55);
        background: linear-gradient(135deg, rgba(37,99,235,.18), rgba(15,23,42,.55));
    }
    .ready-icon { color:#38bdf8; font-size:1.15rem; font-weight:800; }
    .ready-title { color:#e6f1ff; font-weight:700; font-size:.84rem; }
    .ready-desc { color:#94a3b8; font-size:.75rem; margin-top:3px; }
    .sidebar-warning { border-color: rgba(245,158,11,.5); }

</style>
""", unsafe_allow_html=True)

# Define Pages
home_page = st.Page("pages/home.py", title="Home", icon="🏠", default=True)
writing_page = st.Page("pages/writing.py", title="Writing Evaluation", icon="✍️")
speaking_page = st.Page("pages/speaking.py", title="Speaking Evaluation", icon="🎙️")
history_page = st.Page("pages/history.py", title="History", icon="🕒")

# Navigation
pg = st.navigation(
    {
        "Main": [home_page],
        "Evaluations": [writing_page, speaking_page],
        "Dashboard": [history_page],
    }
)



# ===== Sidebar AI / API Details =====
openrouter_ok = bool(os.environ.get("OPENROUTER_API_KEY"))
groq_ok = bool(os.environ.get("GROQ_API_KEY"))

st.sidebar.markdown("""
<div class="sidebar-model-title">AI MODEL YANG DIGUNAKAN</div>
<div class="sidebar-model-card">
    <div class="sidebar-model-heading">
        <span class="model-icon">🤖</span>
        <span>AI Model yang Digunakan</span>
    </div>
    <div class="model-item">
        <div class="model-name">🧠 &nbsp;LLM Evaluasi</div>
        <div class="model-desc">Gemini 2.5 Pro via <span class="model-link">OpenRouter</span></div>
    </div>
    <div class="model-divider"></div>
    <div class="model-item">
        <div class="model-name">🎙️ &nbsp;Speech-to-Text</div>
        <div class="model-desc">Whisper Large v3 via <span class="model-link">Groq</span></div>
    </div>
</div>
<div class="sidebar-model-title api-title">STATUS API</div>
""", unsafe_allow_html=True)

api_status_html = f"""
<div class="sidebar-api-card">
    <div class="api-row">
        <span>OpenRouter API</span>
        <span class="api-status {'ok' if openrouter_ok else 'off'}">{'✓' if openrouter_ok else '!'}</span>
    </div>
    <div class="api-row">
        <span>Groq API</span>
        <span class="api-status {'ok' if groq_ok else 'off'}">{'✓' if groq_ok else '!'}</span>
    </div>
</div>
"""
st.sidebar.markdown(api_status_html, unsafe_allow_html=True)

if openrouter_ok and groq_ok:
    st.sidebar.markdown("""
    <div class="sidebar-ready">
        <div class="ready-icon">ⓘ</div>
        <div>
            <div class="ready-title">Pilih menu di atas untuk mulai evaluasi.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.sidebar.markdown("""
    <div class="sidebar-ready sidebar-warning">
        <div class="ready-icon">!</div>
        <div>
            <div class="ready-title">API belum lengkap</div>
            <div class="ready-desc">Periksa OPENROUTER_API_KEY dan GROQ_API_KEY.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Run navigation
pg.run()
