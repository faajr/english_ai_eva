import streamlit as st
from utils.ai_evaluator import evaluate_writing
from db import get_session, Evaluation

st.title("✍️ Writing Evaluation")
st.markdown("Paste your English writing below to get instant feedback on grammar, vocabulary, and coherence.")

input_text = st.text_area("Your text:", height=200, placeholder="Start typing here...")

if st.button("Evaluate"):
    if not input_text.strip():
        st.warning("Please enter some text to evaluate.")
    else:
        with st.spinner("Evaluating your writing using AI..."):
            result = evaluate_writing(input_text)
            
            if "error" in result:
                st.error(f"Error during evaluation: {result['error']}")
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
                    st.metric("Coherence", f"{result.get('coherence_score', 0)}/100")
                    
                st.markdown("### Feedback")
                st.info(result.get("feedback", "No feedback provided."))
