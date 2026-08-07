import streamlit as st
import os

st.title("⚙️ Settings")
st.markdown("Konfigurasi API Key untuk menjalankan fitur AI Evaluator.")

st.markdown("---")

# ── Load saved keys from env / session state ──────────────────────────────────
def get_key(name):
    return st.session_state.get(name) or os.environ.get(name, "")

# ── OpenRouter ─────────────────────────────────────────────────────────────────
st.markdown("### 🔑 OpenRouter API Key")
st.markdown(
    "Digunakan untuk evaluasi **Writing** dan **Speaking** (LLM: Gemini 2.5 Pro).\n\n"
    "Daftar gratis di 👉 [openrouter.ai](https://openrouter.ai)"
)

openrouter_key = st.text_input(
    "OpenRouter API Key",
    type="password",
    value=get_key("OPENROUTER_API_KEY"),
    placeholder="sk-or-v1-...",
)

st.markdown("---")

# ── Groq ──────────────────────────────────────────────────────────────────────
st.markdown("### 🎙️ Groq API Key")
st.markdown(
    "Digunakan untuk **Speech-to-Text** (Whisper large-v3) di halaman Speaking.\n\n"
    "Daftar gratis di 👉 [console.groq.com](https://console.groq.com)"
)

groq_key = st.text_input(
    "Groq API Key",
    type="password",
    value=get_key("GROQ_API_KEY"),
    placeholder="gsk_...",
)

st.markdown("---")

# ── Save Button ────────────────────────────────────────────────────────────────
if st.button("💾 Simpan API Key", use_container_width=True):
    saved = []
    errors = []

    if openrouter_key.strip():
        st.session_state["OPENROUTER_API_KEY"] = openrouter_key.strip()
        saved.append("✅ OpenRouter API Key")
    else:
        errors.append("⚠️ OpenRouter API Key kosong")

    if groq_key.strip():
        st.session_state["GROQ_API_KEY"] = groq_key.strip()
        saved.append("✅ Groq API Key")
    else:
        errors.append("⚠️ Groq API Key kosong (Speaking tidak akan berfungsi)")

    if saved:
        st.success("\n".join(saved) + "\n\nAPI Key berhasil disimpan! Kamu sekarang bisa menggunakan fitur evaluasi.")
    for e in errors:
        st.warning(e)

st.markdown("---")

# ── Status indicator ──────────────────────────────────────────────────────────
st.markdown("### 📊 Status API Key")

col1, col2 = st.columns(2)
with col1:
    if get_key("OPENROUTER_API_KEY"):
        st.success("🔑 OpenRouter: **Terkonfigurasi** ✅")
    else:
        st.error("🔑 OpenRouter: **Belum diisi** ❌")

with col2:
    if get_key("GROQ_API_KEY"):
        st.success("🎙️ Groq (STT): **Terkonfigurasi** ✅")
    else:
        st.warning("🎙️ Groq (STT): **Belum diisi** ⚠️")

st.markdown("---")

# ── Info box ──────────────────────────────────────────────────────────────────
with st.expander("ℹ️ Cara mendapatkan API Key (klik untuk buka)"):
    st.markdown("""
    **OpenRouter API Key** (untuk evaluasi AI):
    1. Buka [openrouter.ai](https://openrouter.ai)
    2. Daftar / Login
    3. Klik menu **Keys** → **Create Key**
    4. Copy key dan paste di atas

    ---

    **Groq API Key** (untuk Speech-to-Text gratis):
    1. Buka [console.groq.com](https://console.groq.com)
    2. Daftar / Login dengan Google
    3. Klik **API Keys** → **Create API Key**
    4. Copy key dan paste di atas

    > 💡 **Tip:** Kedua layanan ini memiliki free tier yang cukup untuk penggunaan pribadi.
    """)
