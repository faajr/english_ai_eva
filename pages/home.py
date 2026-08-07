import streamlit as st
import os

# --- Hero ---
st.title("🎓 AI English Writing & Speaking Evaluator")
st.markdown("### Selamat datang di tutor bahasa Inggris AI pribadimu!")
st.markdown(
    "Aplikasi ini menggunakan Large Language Model (LLM) canggih untuk membantu kamu "
    "meningkatkan kemampuan bahasa Inggris — **Writing** dan **Speaking**, lengkap dengan "
    "feedback instan dan riwayat progresmu."
)

st.markdown("<br>", unsafe_allow_html=True)

# --- Feature cards ---
st.markdown("#### ✨ Fitur Utama")
col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.markdown("### ✍️")
        st.markdown("**Writing**")
        st.caption("Feedback instan Grammar, Vocabulary & Coherence.")

with col2:
    with st.container(border=True):
        st.markdown("### 🎙️")
        st.markdown("**Speaking**")
        st.caption("Rekam / upload audio → dinilai Fluency, Grammar & Vocabulary.")

with col3:
    with st.container(border=True):
        st.markdown("### 💡")
        st.markdown("**Sample Latihan**")
        st.caption("5 sample teks & 5 sample audio siap pakai.")

with col4:
    with st.container(border=True):
        st.markdown("### 🕒")
        st.markdown("**History & Export**")
        st.caption("Riwayat evaluasi tersimpan otomatis, export ke CSV.")

st.markdown("<br>", unsafe_allow_html=True)

# --- AI Model info ---
with st.container(border=True):
    st.markdown("#### 🤖 AI Model yang Digunakan")
    m1, m2 = st.columns(2)
    with m1:
        st.markdown("**🧠 LLM Evaluasi**")
        st.caption("Gemini 2.5 Pro via [OpenRouter](https://openrouter.ai)")
    with m2:
        st.markdown("**🎙️ Speech-to-Text**")
        st.caption("Whisper Large v3 via [Groq](https://console.groq.com)")

st.markdown("<br>", unsafe_allow_html=True)

# --- API key status ---
openrouter_ok = bool(os.environ.get("OPENROUTER_API_KEY"))
groq_ok = bool(os.environ.get("GROQ_API_KEY"))

if openrouter_ok and groq_ok:
    st.success("✅ Aplikasi siap digunakan!")
    st.info("💡 Gunakan menu di sidebar untuk mulai evaluasi Writing atau Speaking.")
else:
    st.warning("⚠️ API Key belum dikonfigurasi. Aplikasi belum bisa melakukan evaluasi.")
    with st.expander("📋 Cara mengisi API Key di Streamlit Cloud", expanded=True):
        st.markdown("""
        **Langkah-langkah:**

        1. Buka dashboard aplikasimu di [share.streamlit.io](https://share.streamlit.io)
        2. Klik tombol **⋮** (titik tiga) di pojok kanan atas aplikasimu → pilih **Settings**
        3. Klik tab **Secrets**
        4. Tambahkan API key berikut:

        ```toml
        OPENROUTER_API_KEY = "sk-or-v1-xxxxxxxxxxxxxxxx"
        GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxx"
        ```

        5. Klik **Save** → aplikasi akan restart otomatis.

        ---

        **Cara mendapatkan API Key:**

        🔑 **OpenRouter** (untuk evaluasi AI — gratis):
        - Buka [openrouter.ai](https://openrouter.ai) → Login → menu **Keys** → **Create Key**

        🎙️ **Groq** (untuk Speech-to-Text — gratis):
        - Buka [console.groq.com](https://console.groq.com) → Login → **API Keys** → **Create API Key**
        """)
