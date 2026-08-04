import streamlit as st
import os
import time
from utils.ai_evaluator import speech_to_text, evaluate_speaking
from db import get_session, Evaluation

st.title("🎙️ Speaking Evaluation")
st.markdown("Record your voice or upload an audio file to get feedback on your fluency, grammar, and vocabulary.")

# Tabs for input method
tab1, tab2 = st.tabs(["Record Audio", "Upload Audio"])

audio_file = None

with tab1:
    st.markdown("Click the microphone to start recording.")
    # Streamlit 1.39+ native audio input
    recorded_audio = st.audio_input("Record your speaking")
    if recorded_audio:
        audio_file = recorded_audio

with tab2:
    st.markdown("Upload a pre-recorded audio file (e.g., MP3, WAV, M4A).")
    uploaded_audio = st.file_uploader("Upload Audio", type=["mp3", "wav", "m4a", "ogg"])
    if uploaded_audio:
        audio_file = uploaded_audio

if audio_file is not None:
    st.audio(audio_file)
    
    if st.button("Evaluate Audio"):
        # Save audio temporarily
        os.makedirs("data/audio", exist_ok=True)
        timestamp = int(time.time())
        # Try to get extension, default to .wav
        ext = ".wav"
        if hasattr(audio_file, "name"):
            _, ext = os.path.splitext(audio_file.name)
            
        file_path = f"data/audio/audio_{timestamp}{ext}"
        
        with open(file_path, "wb") as f:
            f.write(audio_file.getbuffer())
            
        st.info("Audio saved. Starting transcription...")
        
        with st.spinner("Transcribing using Whisper..."):
            stt_result = speech_to_text(file_path)
            
        if "error" in stt_result:
            st.error(f"Error during transcription: {stt_result['error']}")
        else:
            transcript = stt_result["transcript"]
            st.markdown("### Transcript")
            st.write(transcript)
            
            with st.spinner("Evaluating transcript using AI..."):
                result = evaluate_speaking(transcript)
                
            if "error" in result:
                st.error(f"Error during evaluation: {result['error']}")
            else:
                # Save to database
                try:
                    db = get_session()
                    new_eval = Evaluation(
                        type="speaking",
                        transcript=transcript,
                        audio_path=file_path,
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
                    st.error(f"Failed to save to database: {e}")
                
                # Display results
                st.success("Evaluation complete!")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Overall Score", f"{result.get('overall_score', 0)}/100")
                with col2:
                    st.metric("Grammar", f"{result.get('grammar_score', 0)}/100")
                with col3:
                    st.metric("Vocabulary", f"{result.get('vocabulary_score', 0)}/100")
                with col4:
                    st.metric("Fluency", f"{result.get('fluency_score', 0)}/100")
                    
                st.markdown("### Feedback")
                st.info(result.get("feedback", "No feedback provided."))
