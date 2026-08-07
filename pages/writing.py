import streamlit as st
from utils.ai_evaluator import evaluate_writing
from db import get_session, Evaluation
import os

# --- Load Sample Texts ---
# os.getcwd() returns the app root on both local and Streamlit Cloud
SAMPLE_DIR = os.path.join(os.getcwd(), "data")

def load_sample_texts():
    samples = {}
    sample_files = {
        "📖 Sample 1 – Future Plans": "text1.txt",
        "🌴 Sample 2 – Bali & Lombok": "text2.txt",
        "🚗 Sample 3 – Daily Routine": "text3.txt",
        "🛒 Sample 4 – At the Grocery Store": "text4.txt",
    }
    for label, fname in sample_files.items():
        fpath = os.path.join(SAMPLE_DIR, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                samples[label] = f.read().strip()
    return samples

SAMPLE_TEXTS = load_sample_texts()

# --- Page Layout ---
st.title("✍️ Writing Evaluation")
st.markdown("Tulis atau paste teks bahasa Inggrismu untuk mendapatkan feedback dari AI.")

# Initialize input text (must be before sample picker)
if "writing_input" not in st.session_state:
    st.session_state["writing_input"] = ""

# Sample Picker
st.markdown("#### 💡 Gunakan Sample Latihan")

if not SAMPLE_TEXTS:
    st.warning(f"⚠️ Sample teks tidak ditemukan di folder `data/`. (Path: `{SAMPLE_DIR}`)")
else:
    sample_labels = ["– Pilih sample teks –"] + list(SAMPLE_TEXTS.keys())
    selected_sample = st.selectbox("Pilih sample:", sample_labels)

    # Fill textarea when sample is selected
    if selected_sample != "– Pilih sample teks –":
        st.session_state["writing_input"] = SAMPLE_TEXTS[selected_sample]

input_text = st.text_area(
    "Teks kamu:",
    value=st.session_state["writing_input"],
    height=200,
    placeholder="Mulai ketik atau pilih sample di atas...",
    key="writing_textarea"
)

col_btn1, col_btn2 = st.columns([1, 5])
with col_btn1:
    evaluate_clicked = st.button("🚀 Evaluate")
with col_btn2:
    if st.button("🗑️ Clear"):
        st.session_state["writing_input"] = ""
        st.rerun()

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
