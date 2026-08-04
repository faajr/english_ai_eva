import streamlit as st

# Setup page config (Must be the first Streamlit command)
st.set_page_config(
    page_title="AI English Evaluator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "modern hi tech"
st.markdown("""
<style>
    /* Global font and background */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;700&family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        color: #e0e0e0;
    }
    
    /* Main background */
    .stApp {
        background-color: #0b0f19;
        background-image: 
            radial-gradient(circle at 15% 50%, rgba(0, 255, 255, 0.05), transparent 25%),
            radial-gradient(circle at 85% 30%, rgba(138, 43, 226, 0.05), transparent 25%);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border-right: 1px solid rgba(0, 255, 255, 0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Orbitron', sans-serif;
        color: #00ffff;
        font-weight: 500;
        text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
        letter-spacing: 1px;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #0f172a 0%, #1e293b 100%);
        color: #00ffff;
        border-radius: 4px;
        border: 1px solid rgba(0, 255, 255, 0.5);
        padding: 0.5rem 1rem;
        font-weight: 600;
        font-family: 'Orbitron', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(0, 255, 255, 0.1);
    }
    
    .stButton>button:hover {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(0, 255, 255, 0.4);
        border-color: #00ffff;
        color: #ffffff;
    }
    
    /* Text areas and inputs */
    .stTextArea>div>div>textarea, .stTextInput>div>div>input {
        border-radius: 4px;
        border: 1px solid rgba(0, 255, 255, 0.2);
        background-color: rgba(15, 23, 42, 0.6);
        color: #00ffff;
        padding: 0.75rem;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextArea>div>div>textarea:focus, .stTextInput>div>div>input:focus {
        border-color: #00ffff;
        box-shadow: 0 0 0 2px rgba(0, 255, 255, 0.2);
    }

    /* Cards / Containers */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        background: rgba(15, 23, 42, 0.4);
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        border: 1px solid rgba(0, 255, 255, 0.1);
        backdrop-filter: blur(5px);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #00ffff !important;
        font-family: 'Orbitron', sans-serif;
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
    }
    
    /* Metric Card styling via Streamlit is tricky, but we target its parent if possible. 
       We rely on general text coloring for metrics. */
       
    /* Override markdown text colors */
    .stMarkdown, p, li {
        color: #cbd5e1;
    }
    
    /* Info / Success alerts */
    .stAlert {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border: 1px solid rgba(0, 255, 255, 0.3) !important;
        color: #e0e0e0 !important;
    }
</style>
""", unsafe_allow_html=True)

# API Key Configuration in Sidebar
with st.sidebar:
    st.markdown("### ⚙️ API Configuration")
    
    openrouter_key = st.text_input("OpenRouter API Key (For AI Evaluation)", type="password", value=st.session_state.get("OPENROUTER_API_KEY", ""))
    if openrouter_key:
        st.session_state["OPENROUTER_API_KEY"] = openrouter_key
        
    openai_key = st.text_input("OpenAI API Key (Optional for STT)", type="password", value=st.session_state.get("OPENAI_API_KEY", ""))
    if openai_key:
        st.session_state["OPENAI_API_KEY"] = openai_key
        
    st.markdown("---")

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
