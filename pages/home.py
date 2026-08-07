import streamlit as st
import os

st.title("🎓 AI English Writing & Speaking Evaluator")
st.markdown("### Selamat datang di tutor bahasa Inggris AI pribadimu!")

st.markdown("""
Aplikasi ini menggunakan Large Language Model (LLM) canggih untuk membantu kamu meningkatkan kemampuan bahasa Inggris — Writing dan Speaking.

**Fitur Utama:**
- ✍️ **Writing Evaluation** — Feedback instan tentang Grammar, Vocabulary, dan Coherence.
- 🎙️ **Speaking Evaluation** — Rekam atau upload audio, AI evaluasi Fluency, Grammar, dan Vocabulary.
- 💡 **Sample Latihan** — 4 sample teks dan 4 sample audio siap digunakan.
- 🕒 **History** — Semua hasil evaluasi tersimpan otomatis.
- 📊 **Export CSV** — Download riwayat evaluasi dalam format CSV.

**AI Model:**
- 🤖 **LLM:** Gemini 2.5 Pro via [OpenRouter](https://openrouter.ai)
- 🎙️ **STT:** Whisper Large v3 via [Groq](https://console.groq.com)
""")

# Check API key status
openrouter_ok = bool(os.environ.get("OPENROUTER_API_KEY"))
groq_ok = bool(os.environ.get("GROQ_API_KEY"))

st.markdown("---")

if openrouter_ok and groq_ok:
    st.success("✅ Semua API Key sudah terkonfigurasi. Aplikasi siap digunakan!")
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
