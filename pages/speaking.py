import streamlit as st
import os
import time
from utils.ai_evaluator import speech_to_text, evaluate_speaking
from db import get_session, Evaluation

# --- Sample Audio Files ---
# os.getcwd() returns the app root on both local and Streamlit Cloud
SAMPLE_DIR = os.path.join(os.getcwd(), "data")

AUDIO_EXTENSIONS = (".mp3", ".wav", ".m4a", ".ogg", ".flac")

def load_sample_audios():
    """Auto-scan folder data/ untuk semua file audio"""
    samples = {}
    if not os.path.exists(SAMPLE_DIR):
        return samples
    audio_files = sorted([
        f for f in os.listdir(SAMPLE_DIR)
        if f.lower().endswith(AUDIO_EXTENSIONS)
    ])
    for fname in audio_files:
        label = f"🎧 {os.path.splitext(fname)[0]}"  # nama file tanpa ekstensi
        samples[label] = os.path.join(SAMPLE_DIR, fname)
    return samples

SAMPLE_AUDIOS = load_sample_audios()

# --- Page Layout ---
st.title("🎙️ Speaking Evaluation")
st.markdown("Rekam suaramu atau upload file audio, lalu dapatkan feedback dari AI tentang fluency, grammar, dan vocabulary.")

# --- Input card ---
with st.container(border=True):
    # Tabs: Record | Upload | Sample
    tab1, tab2, tab3 = st.tabs(["🎤 Rekam Suara", "📂 Upload Audio", "💡 Sample Latihan"])

    audio_file = None
    audio_file_bytes = None
    sample_audio_path = None  # Path string for sample files

    with tab1:
        st.markdown("Klik tombol mikrofon untuk mulai merekam.")
        recorded_audio = st.audio_input("Rekam suaramu:")
        if recorded_audio:
            audio_file = recorded_audio

    with tab2:
        st.markdown("Upload file audio kamu (MP3, WAV, M4A, OGG).")
        uploaded_audio = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a", "ogg"])
        if uploaded_audio:
            audio_file = uploaded_audio

    with tab3:
        st.markdown("Gunakan file audio sample berikut untuk mencoba fitur Speaking Evaluation.")

        if not SAMPLE_AUDIOS:
            st.warning(f"⚠️ Tidak ada file audio di folder `data/`. (Path: `{SAMPLE_DIR}`)")
        else:
            sample_labels = ["– Pilih sample audio –"] + list(SAMPLE_AUDIOS.keys())
            selected_sample = st.selectbox("Pilih sample:", sample_labels, key="speaking_sample")

            if selected_sample != "– Pilih sample audio –":
                fpath = SAMPLE_AUDIOS[selected_sample]  # sudah full path
                if os.path.exists(fpath):
                    st.audio(fpath)
                    sample_audio_path = fpath
                    st.success(f"✅ Sample dipilih: **{selected_sample}**")
                else:
                    st.error(f"File tidak ditemukan: {fpath}")

    # --- Main Evaluation Logic ---
    # Determine which audio source is active
    has_audio = (audio_file is not None) or (sample_audio_path is not None)

    if audio_file is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        st.audio(audio_file)

    if has_audio:
        st.markdown("<br>", unsafe_allow_html=True)
        evaluate_clicked = st.button("🚀 Evaluate Audio", type="primary")
    else:
        evaluate_clicked = False
        st.info("👆 Pilih salah satu tab di atas: rekam suara, upload file, atau pilih sample latihan.")

if has_audio and evaluate_clicked:
    # Save audio to temp path
    os.makedirs(os.path.join(SAMPLE_DIR, "audio_uploads"), exist_ok=True)
    timestamp = int(time.time())

    if sample_audio_path:
        # Use sample directly
        save_path = sample_audio_path
    else:
        # Save uploaded/recorded audio
        ext = ".wav"
        if hasattr(audio_file, "name"):
            _, ext = os.path.splitext(audio_file.name)
            if not ext:
                ext = ".wav"
        save_path = os.path.join(SAMPLE_DIR, "audio_uploads", f"audio_{timestamp}{ext}")
        with open(save_path, "wb") as f:
            f.write(audio_file.getbuffer())

    # Step 1: Transcribe
    with st.spinner("🔤 Mentranskripsi audio dengan Whisper (Groq)..."):
        stt_result = speech_to_text(save_path)

    if "error" in stt_result:
        st.error(f"❌ Error transkripsi: {stt_result['error']}")
    else:
        transcript = stt_result["transcript"]

        with st.container(border=True):
            st.markdown("#### 🔤 Hasil Transkripsi")
            st.write(transcript)

        # Step 2: Evaluate
        with st.spinner("🤖 AI sedang mengevaluasi speaking kamu..."):
            result = evaluate_speaking(transcript)

        if "error" in result:
            st.error(f"❌ Error evaluasi: {result['error']}")
        else:
            # Save to database
            try:
                db = get_session()
                new_eval = Evaluation(
                    type="speaking",
                    transcript=transcript,
                    audio_path=save_path,
                    grammar_score=result.get("grammar_score", 0),
                    vocabulary_score=result.get("vocabulary_score", 0),
                    fluency_score=result.get("fluency_score", 0),
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
            st.markdown("<br>", unsafe_allow_html=True)

            with st.container(border=True):
                st.markdown("#### 📊 Hasil Evaluasi")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🏆 Overall", f"{result.get('overall_score', 0)}/100")
                with col2:
                    st.metric("📝 Grammar", f"{result.get('grammar_score', 0)}/100")
                with col3:
                    st.metric("📚 Vocabulary", f"{result.get('vocabulary_score', 0)}/100")
                with col4:
                    st.metric("🗣️ Fluency", f"{result.get('fluency_score', 0)}/100")

                st.markdown("#### 💬 Feedback AI")
                st.info(result.get("feedback", "Tidak ada feedback."))
