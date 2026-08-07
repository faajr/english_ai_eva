import streamlit as st
from utils.ai_evaluator import evaluate_writing
from db import get_session, Evaluation
import os

# --- Load Sample Texts ---
SAMPLE_DIR = os.path.join(os.getcwd(), "data")

def load_sample_texts():
    """Auto-scan folder data/ untuk semua file .txt"""
    samples = {}
    if not os.path.exists(SAMPLE_DIR):
        return samples
    txt_files = sorted([f for f in os.listdir(SAMPLE_DIR) if f.endswith(".txt")])
    for fname in txt_files:
        label = f"📄 {os.path.splitext(fname)[0]}"  # nama file tanpa ekstensi
        fpath = os.path.join(SAMPLE_DIR, fname)
        with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
            samples[label] = f.read().strip()
    return samples

SAMPLE_TEXTS = load_sample_texts()

# --- Page Layout ---
st.title("✍️ Writing Evaluation")
st.markdown("Tulis atau paste teks bahasa Inggrismu untuk mendapatkan feedback dari AI.")

# --- Initialize session state ---
if "writing_textarea" not in st.session_state:
    st.session_state["writing_textarea"] = ""
if "selected_sample_prev" not in st.session_state:
    st.session_state["selected_sample_prev"] = ""
if "clear_writing" not in st.session_state:
    st.session_state["clear_writing"] = False

# Clear flag must be handled BEFORE the textarea widget is rendered
if st.session_state["clear_writing"]:
    st.session_state["writing_textarea"] = ""
    st.session_state["selected_sample_prev"] = ""
    st.session_state["clear_writing"] = False

# --- Sample Picker ---
st.markdown("#### 💡 Gunakan Sample Latihan")

if not SAMPLE_TEXTS:
    st.warning(f"⚠️ Sample teks tidak ditemukan. (Path: `{SAMPLE_DIR}`)")
else:
    sample_labels = ["– Pilih sample teks –"] + list(SAMPLE_TEXTS.keys())
    selected_sample = st.selectbox("Pilih sample:", sample_labels, key="sample_selectbox")

    # Detect new selection → update textarea + rerun to reflect change
    if selected_sample != "– Pilih sample teks –" and selected_sample != st.session_state["selected_sample_prev"]:
        st.session_state["writing_textarea"] = SAMPLE_TEXTS[selected_sample]
        st.session_state["selected_sample_prev"] = selected_sample
        st.rerun()

# --- Text Area (key controls its own state) ---
input_text = st.text_area(
    "Teks kamu:",
    height=220,
    placeholder="Mulai ketik di sini atau pilih sample latihan di atas...",
    key="writing_textarea"
)

# --- Buttons ---
col_btn1, col_btn2 = st.columns([1, 5])
with col_btn1:
    evaluate_clicked = st.button("🚀 Evaluate")
with col_btn2:
    if st.button("🗑️ Clear"):
        st.session_state["clear_writing"] = True
        st.rerun()

# --- Evaluation ---
if evaluate_clicked:
    if not input_text.strip():
        st.warning("⚠️ Silakan masukkan teks terlebih dahulu.")
    else:
        with st.spinner("🤖 AI sedang mengevaluasi tulisanmu..."):
            result = evaluate_writing(input_text)

        if "error" in result:
            st.error(f"❌ Error: {result['error']}")
        else:
            # Save to database
            try:
                db = get_session()
                new_eval = Evaluation(
                    type="writing",
                    input_text=input_text,
                    grammar_score=result.get("grammar_score", 0),
                    vocabulary_score=result.get("vocabulary_score", 0),
                    coherence_score=result.get("coherence_score", 0),
                    overall_score=result.get("overall_score", 0),
                    feedback=result.get("feedback", "")
                )
                db.add(new_eval)
                db.commit()
                db.close()
            except Exception as e:
                st.warning(f"⚠️ Gagal menyimpan ke database: {e}")

            # Display results
            st.success("✅ Evaluasi selesai!")
            st.markdown("---")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🏆 Overall", f"{result.get('overall_score', 0)}/100")
            with col2:
                st.metric("📝 Grammar", f"{result.get('grammar_score', 0)}/100")
            with col3:
                st.metric("📚 Vocabulary", f"{result.get('vocabulary_score', 0)}/100")
            with col4:
                st.metric("🔗 Coherence", f"{result.get('coherence_score', 0)}/100")

            st.markdown("### 💬 Feedback AI")
            st.info(result.get("feedback", "Tidak ada feedback."))
