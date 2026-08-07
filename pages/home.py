import streamlit as st

st.title("🎓 AI English Writing & Speaking Evaluator")
st.markdown("### Selamat datang di tutor bahasa Inggris AI pribadimu!")

st.markdown("""
Aplikasi ini menggunakan Large Language Model (LLM) canggih untuk membantu kamu meningkatkan kemampuan bahasa Inggris secara menyeluruh — Writing dan Speaking.

**Fitur Utama:**
- ✍️ **Writing Evaluation** — Dapatkan feedback instan tentang Grammar, Vocabulary, dan Coherence tulisanmu.
- 🎙️ **Speaking Evaluation** — Rekam atau upload audio, lalu AI akan mengevaluasi Fluency, Grammar, dan Vocabulary bicaramu.
- 💡 **Sample Latihan** — Tersedia 4 sample teks dan 4 sample audio untuk langsung dicoba.
- 🕒 **History** — Semua hasil evaluasi tersimpan otomatis agar kamu bisa memantau progres.
- 📊 **Export CSV** — Download seluruh riwayat evaluasimu dalam format CSV.

**AI Model yang digunakan:**
- 🤖 **LLM Evaluator:** Gemini 2.5 Pro (via [OpenRouter](https://openrouter.ai))
- 🎙️ **Speech-to-Text:** Whisper Large v3 (via [Groq](https://console.groq.com) — gratis & cepat)

---
> ⚙️ **Sebelum mulai**, pastikan kamu sudah mengisi API Key di halaman **Settings** (menu di sidebar kiri).

💡 **Tip:** Berbicaralah dengan jelas dan natural saat menggunakan fitur Speaking Evaluation untuk hasil terbaik!
""")
