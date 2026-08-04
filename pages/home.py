import streamlit as st

st.title("🎓 AI English Writing & Speaking Evaluator")
st.markdown("### Welcome to your personal AI English tutor!")

st.markdown("""
This application uses advanced Large Language Models to help you improve your English skills.

**Features:**
- ✍️ **Writing Evaluation:** Get instant feedback on your grammar, vocabulary, and coherence.
- 🎙️ **Speaking Evaluation:** Practice your speaking and get feedback on your fluency and accuracy (Speech-to-Text powered by Whisper).
- 🕒 **History Tracking:** Save all your evaluations to track your progress over time.
- 📊 **Export Data:** Export your scores and feedback to CSV for offline analysis.

**AI Models Used:**
- **LLM:** Gemini 2.5 Pro (via Google GenAI)
- **STT:** Whisper (via OpenAI API)

Navigate using the sidebar to get started!
""")

# Decorative element
st.info("💡 Tip: Try to speak naturally and clearly when using the Speaking Evaluation feature for the best results.")
