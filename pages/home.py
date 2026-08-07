import os
import streamlit as st

# ============================================================
# HOME — AI English Evaluator
# ============================================================

# API status: support both Streamlit Secrets and environment variables
def get_secret(name: str) -> str:
    try:
        value = st.secrets.get(name, "")
        if value:
            return str(value)
    except Exception:
        pass
    return os.environ.get(name, "")

openrouter_ok = bool(get_secret("OPENROUTER_API_KEY"))
groq_ok = bool(get_secret("GROQ_API_KEY"))

# ============================================================
# Sidebar — model information
# ============================================================

st.sidebar.markdown("""
<style>
.sidebar-brand {
    padding: 8px 4px 20px 4px;
}

.sidebar-brand-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: #00f5ff;
    margin: 0;
}

.sidebar-brand-subtitle {
    color: #94a3b8;
    font-size: 0.9rem;
    margin-top: 4px;
}

.sidebar-section-title {
    margin: 22px 0 12px 4px;
    color: #94a3b8;
    font-size: 0.82rem;
    font-weight: 700;
    letter-spacing: 1.5px;
}

.sidebar-model-card {
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(148, 163, 184, 0.35);
    background: linear-gradient(
        145deg,
        rgba(15, 23, 42, 0.9),
        rgba(8, 15, 30, 0.8)
    );
    box-shadow:
        0 10px 30px rgba(0, 0, 0, 0.25),
        inset 0 1px 0 rgba(255, 255, 255, 0.03);
}

.sidebar-model-heading {
    display: flex;
    align-items: center;
    gap: 9px;
    color: #00f5ff;
    font-size: 1rem;
    font-weight: 800;
    margin-bottom: 22px;
}

.model-item {
    padding: 2px 0;
}

.model-name {
    color: #e6f1ff;
    font-size: 0.92rem;
    font-weight: 700;
    margin-bottom: 7px;
}

.model-desc {
    color: #94a3b8;
    font-size: 0.8rem;
    line-height: 1.5;
}

.model-link {
    color: #3b82f6;
    text-decoration: underline;
}

.model-divider {
    height: 1px;
    margin: 17px 0;
    background: rgba(148, 163, 184, 0.2);
}

.sidebar-api-card {
    padding: 8px 14px;
    border-radius: 16px;
    border: 1px solid rgba(148, 163, 184, 0.28);
    background: rgba(15, 23, 42, 0.55);
}

.api-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    padding: 10px 0;
    color: #cbd5e1;
    font-size: 0.82rem;
}

.api-status {
    width: 30px;
    height: 30px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    font-weight: 800;
    font-size: 1rem;
}

.api-status.ok {
    color: #22c55e;
    border: 2px solid #22c55e;
    background: rgba(34, 197, 94, 0.08);
}

.api-status.off {
    color: #f59e0b;
    border: 2px solid #f59e0b;
    background: rgba(245, 158, 11, 0.08);
}

.sidebar-ready {
    margin-top: 14px;
    padding: 13px 14px;
    border-radius: 14px;
    border: 1px solid rgba(59, 130, 246, 0.5);
    background: rgba(30, 64, 175, 0.16);
}

.sidebar-ready-title {
    color: #e0f2fe;
    font-weight: 700;
    font-size: 0.82rem;
}

.sidebar-ready-text {
    color: #94a3b8;
    font-size: 0.72rem;
    margin-top: 4px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
<div class="sidebar-brand">
    <div class="sidebar-brand-title">🤖 AI English Evaluator</div>
    <div class="sidebar-brand-subtitle">Write. Speak. Improve.</div>
</div>

<div class="sidebar-section-title">AI MODEL YANG DIGUNAKAN</div>

<div class="sidebar-model-card">
    <div class="sidebar-model-heading">
        <span>🤖</span>
        <span>AI Model yang Digunakan</span>
    </div>

    <div class="model-item">
        <div class="model-name">🧠 &nbsp;LLM Evaluasi</div>
        <div class="model-desc">
            Gemini 2.5 Pro via
            <span class="model-link">OpenRouter</span>
        </div>
    </div>

    <div class="model-divider"></div>

    <div class="model-item">
        <div class="model-name">🎙️ &nbsp;Speech-to-Text</div>
        <div class="model-desc">
            Whisper Large v3 via
            <span class="model-link">Groq</span>
        </div>
    </div>
</div>

<div class="sidebar-section-title">STATUS API</div>
""", unsafe_allow_html=True)

api_status_html = f"""
<div class="sidebar-api-card">
    <div class="api-row">
        <span>OpenRouter API</span>
        <span class="api-status {'ok' if openrouter_ok else 'off'}">
            {'✓' if openrouter_ok else '!'}
        </span>
    </div>
    <div class="api-row">
        <span>Groq API</span>
        <span class="api-status {'ok' if groq_ok else 'off'}">
            {'✓' if groq_ok else '!'}
        </span>
    </div>
</div>

<div class="sidebar-ready">
    <div class="sidebar-ready-title">
        {'✓ Semua sistem siap digunakan!' if openrouter_ok and groq_ok else '⚠ API Key belum lengkap'}
    </div>
    <div class="sidebar-ready-text">
        {'Pilih menu di atas untuk mulai evaluasi.' if openrouter_ok and groq_ok else 'Tambahkan API Key melalui Streamlit Secrets.'}
    </div>
</div>
"""

st.sidebar.markdown(api_status_html, unsafe_allow_html=True)

# ============================================================
# Hero
# ============================================================

st.markdown("""
<div class="hero">
    <div style="display:flex; justify-content:space-between; align-items:center;
                gap:24px; flex-wrap:wrap;">

        <div style="flex:1; min-width:260px;">

            <div style="display:inline-block; padding:6px 12px;
                        border-radius:999px;
                        background:rgba(96,165,250,0.18);
                        border:1px solid rgba(96,165,250,0.35);
                        color:#bfdbfe; font-size:0.85rem;
                        font-weight:700; margin-bottom:16px;">
                ⚡ NEXT-GEN AI EVALUATION
            </div>

            <h1 style="font-size:3rem; line-height:1.05;
                       margin:0 0 12px 0;">
                AI English Writing &amp; Speaking Evaluator
            </h1>

            <p style="font-size:1.05rem; color:#cbd5e1;
                      margin:0 0 22px 0; max-width:720px;">
                Evaluate grammar, vocabulary, fluency, and speaking performance
                with a futuristic AI dashboard designed for modern learners.
            </p>

            <div style="display:flex; gap:12px; flex-wrap:wrap;">
                <div style="padding:10px 14px; border-radius:14px;
                            background:rgba(15,23,42,0.55);
                            border:1px solid rgba(255,255,255,0.08);
                            color:#e2e8f0; font-weight:600;">
                    🧠 Gemini AI
                </div>

                <div style="padding:10px 14px; border-radius:14px;
                            background:rgba(15,23,42,0.55);
                            border:1px solid rgba(255,255,255,0.08);
                            color:#e2e8f0; font-weight:600;">
                    🎤 Whisper STT
                </div>

                <div style="padding:10px 14px; border-radius:14px;
                            background:rgba(15,23,42,0.55);
                            border:1px solid rgba(255,255,255,0.08);
                            color:#e2e8f0; font-weight:600;">
                    📊 Smart Analytics
                </div>
            </div>
        </div>

        <div style="width:260px; min-width:220px;">
            <div style="background:rgba(15,23,42,0.55);
                        border:1px solid rgba(255,255,255,0.10);
                        border-radius:24px; padding:24px;
                        text-align:center;
                        box-shadow:0 0 30px rgba(96,165,250,0.18);">

                <div style="font-size:3rem; margin-bottom:10px;">🚀</div>

                <div style="font-size:1.1rem; font-weight:700;
                            color:#f8fafc;">
                    Ready to Evaluate
                </div>

                <div style="color:#94a3b8; margin-top:6px;">
                    Writing • Speaking • History
                </div>

                <div style="margin-top:18px; padding:10px 12px;
                            border-radius:14px;
                            background:linear-gradient(
                                135deg,
                                rgba(37,99,235,0.25),
                                rgba(139,92,246,0.25)
                            );
                            border:1px solid rgba(255,255,255,0.10);
                            color:#dbeafe; font-weight:700;">
                    ⚡ AI Powered
                </div>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# Feature cards
# ============================================================

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

# ============================================================
# AI model information
# ============================================================

with st.container(border=True):
    st.markdown("#### 🤖 AI Model yang Digunakan")

    m1, m2 = st.columns(2)

    with m1:
        st.markdown("**🧠 LLM Evaluasi**")
        st.caption("Gemini 2.5 Pro via OpenRouter")

    with m2:
        st.markdown("**🎙️ Speech-to-Text**")
        st.caption("Whisper Large v3 via Groq")

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# API information
# ============================================================

if openrouter_ok and groq_ok:
    st.success("✅ Aplikasi siap digunakan!")
    st.info("💡 Gunakan menu di sidebar untuk mulai evaluasi Writing atau Speaking.")
else:
    st.warning("⚠️ API Key belum dikonfigurasi lengkap.")
    with st.expander("📋 Cara mengisi API Key di Streamlit Cloud"):
        st.markdown("""
**Tambahkan API key di Streamlit Cloud → Settings → Secrets:**

```toml
OPENROUTER_API_KEY = "sk-or-v1-xxxxxxxxxxxxxxxx"
GROQ_API_KEY = "gsk_xxxxxxxxxxxxxxxx"
```

Setelah menyimpan Secrets, aplikasi akan restart otomatis.
""")
