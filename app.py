import streamlit as st

# Setup page config (Must be the first Streamlit command)
st.set_page_config(
    page_title="AI English Evaluator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for "modern hi tech simple colour pastel minimalist"
st.markdown("""
<style>
    /* Global font and background */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main background */
    .stApp {
        background-color: #fcfcfc;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #f4f6fa;
        border-right: 1px solid #e1e4e8;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #2c3e50;
        font-weight: 600;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #b5c7d3; /* Pastel blue-grey */
        color: #2c3e50;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #9cb1bf;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        color: #1a252f;
    }
    
    /* Text areas and inputs */
    .stTextArea>div>div>textarea, .stTextInput>div>div>input {
        border-radius: 8px;
        border: 1px solid #e1e4e8;
        background-color: #ffffff;
        padding: 0.75rem;
    }
    
    .stTextArea>div>div>textarea:focus, .stTextInput>div>div>input:focus {
        border-color: #b5c7d3;
        box-shadow: 0 0 0 2px rgba(181, 199, 211, 0.2);
    }

    /* Cards / Containers */
    div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column;"] > div[data-testid="stVerticalBlock"] {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.03);
        border: 1px solid #f0f2f5;
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
