import streamlit as st

# Setup page config (Must be the first Streamlit command)
st.set_page_config(
    page_title="AI English Evaluator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - "hi-tech dark futuristic" theme with neon accents & glassmorphism
st.markdown("""
<style>
    /* Fonts: Space Grotesk for headers (techy), Inter for body */
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }

    /* Main background - deep space navy with subtle radial glow */
    .stApp {
        background:
            radial-gradient(circle at 15% 10%, rgba(0, 229, 255, 0.08) 0%, transparent 40%),
            radial-gradient(circle at 85% 90%, rgba(157, 78, 255, 0.10) 0%, transparent 45%),
            linear-gradient(180deg, #05070d 0%, #0a0e17 100%);
        color: #e6edf5;
    }

    /* Sidebar - glass panel */
    [data-testid="stSidebar"] {
        background: rgba(13, 18, 30, 0.85);
        backdrop-filter: blur(16px);
        border-right: 1px solid rgba(0, 229, 255, 0.15);
    }

    [data-testid="stSidebar"] * {
        color: #c9d6e8 !important;
    }

    /* Headers - gradient neon text */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 600;
        background: linear-gradient(90deg, #00e5ff 0%, #9d4eff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: 0.3px;
    }

    /* Body text */
    p, span, label, .stMarkdown {
        color: #c9d6e8;
    }

    /* Buttons - neon glass */
    .stButton>button {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.15), rgba(157, 78, 255, 0.15));
        color: #00e5ff;
        border-radius: 10px;
        border: 1px solid rgba(0, 229, 255, 0.4);
        padding: 0.55rem 1.1rem;
        font-weight: 600;
        letter-spacing: 0.3px;
        transition: all 0.25s ease;
        box-shadow: 0 0 0 rgba(0, 229, 255, 0);
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.3), rgba(157, 78, 255, 0.3));
        border-color: rgba(0, 229, 255, 0.8);
        color: #ffffff;
        transform: translateY(-2px);
        box-shadow: 0 4px 20px rgba(0, 229, 255, 0.35);
    }

    /* Text areas and inputs - dark glass fields with neon focus ring */
    .stTextArea>div>div>textarea, .stTextInput>div>div>input {
        font-family: 'JetBrains Mono', monospace;
        border-radius: 10px;
        border: 1px solid rgba(0, 229, 255, 0.2);
        background-color: rgba(13, 18, 30, 0.75);
        color: #e6edf5;
        padding: 0.85rem;
    }

    .stTextArea>div>div>textarea:focus, .stTextInput>div>div>input:focus {
        border-color: #00e5ff;
        box-shadow: 0 0 0 3px rgba(0, 229, 255, 0.2);
    }

    /* Cards / Containers - glassmorphism with neon border glow */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        background: rgba(17, 22, 36, 0.65);
        backdrop-filter: blur(14px);
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35), 0 0 0 1px rgba(0, 229, 255, 0.08) inset;
        border: 1px solid rgba(0, 229, 255, 0.15);
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background: rgba(17, 22, 36, 0.65);
        border: 1px solid rgba(157, 78, 255, 0.25);
        border-radius: 12px;
        padding: 1rem;
    }

    [data-testid="stMetricValue"] {
        color: #00e5ff;
        font-family: 'Space Grotesk', sans-serif;
    }

    /* Dataframes / tables */
    [data-testid="stDataFrame"] {
        border: 1px solid rgba(0, 229, 255, 0.15);
        border-radius: 10px;
    }

    /* Progress bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00e5ff, #9d4eff);
    }

    /* Divider glow */
    hr {
        border-color: rgba(0, 229, 255, 0.2);
    }
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
        "Dashboard": [history_page]
    }
)

# Run navigation
pg.run()
