import streamlit as st
import os

# --- Hero ---
st.markdown("""<div class="hero">
            <div style="display:flex; justify-content:space-between; align-items:center; gap:24px; flex-wrap:wrap;">
                <div style="flex:1; min-width:260px;">
                    <div style="display:inline-block; padding:6px 12px; border-radius:999px; background:rgba(96,165,250,0.18); border:1px solid rgba(96,165,250,0.35); color:#bfdbfe; font-size:0.85rem; font-weight:700; margin-bottom:16px;">
                        ⚡ NEXT-GEN AI EVALUATION
                    </div>
                    <h1 style="font-size:3rem; line-height:1.05; margin:0 0 12px 0;">AI English Writing &amp; Speaking Evaluator</h1>
                    <p style="font-size:1.05rem; color:#cbd5e1; margin:0 0 22px 0; max-width:720px;">
                        Evaluate grammar, vocabulary, fluency, and speaking performance with a futuristic AI dashboard designed for modern learners.
                    </p>
                    <div style="display:flex; gap:12px; flex-wrap:wrap;">
                        <div style="padding:10px 14px; border-radius:14px; background:rgba(15,23,42,0.55); border:1px solid rgba(255,255,255,0.08); color:#e2e8f0; font-weight:600;">🧠 Gemini AI</div>
                        <div style="padding:10px 14px; border-radius:14px; background:rgba(15,23,42,0.55); border:1px solid rgba(255,255,255,0.08); color:#e2e8f0; font-weight:600;">🎤 Whisper STT</div>
                        <div style="padding:10px 14px; border-radius:14px; background:rgba(15,23,42,0.55); border:1px solid rgba(255,255,255,0.08); color:#e2e8f0; font-weight:600;">📊 Smart Analytics</div>
                    </div>
                </div>
                <div style="width:260px; min-width:220px;">
                    <div style="background:rgba(15,23,42,0.55); border:1px solid rgba(255,255,255,0.10); border-radius:24px; padding:24px; text-align:center; box-shadow:0 0 30px rgba(96,165,250,0.18);">
                        <div style="font-size:3rem; margin-bottom:10px;">🚀</div>
                        <div style="font-size:1.1rem; font-weight:700; color:#f8fafc;">Ready to Evaluate</div>
                        <div style="color:#94a3b8; margin-top:6px;">Writing • Speaking • History</div>
                        <div style="margin-top:18px; padding:10px 12px; border-radius:14px; background:linear-gradient(135deg, rgba(37,99,235,0.25), rgba(139,92,246,0.25)); border:1px solid rgba(255,255,255,0.10); color:#dbeafe; font-weight:700;">⚡ AI Powered</div>
                    </div>
                </div>
            </div>
            <p></p>
        </div>""", unsafe_allow_html=True)

# --- Feature cards ---
st.markdown("#### ✨ Fitur Utama")
col1, col2, col3, col4 = st.columns(4)

with col1:
    with st.container(border=True):
        st.markdown("### ✍️")
        st.markdown("**Writing Evaluation**")
        st.caption("Feedback instan Grammar, Vocabulary & Coherence.")

with col2:
    with st.container(border=True):
        st.markdown("### 🎙️")
        st.markdown("**Speaking Evaluation**")
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

# --- API key status ---
openrouter_ok = bool(os.environ.get("OPENROUTER_API_KEY"))
groq_ok = bool(os.environ.get("GROQ_API_KEY"))

# --- Sidebar API status ---
st.sidebar.markdown("""
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
    st.success("✅ Aplikasi siap digunakan!")
    st.info("")
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
