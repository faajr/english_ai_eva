import streamlit as st
import pandas as pd
from sqlalchemy.orm import class_mapper
from db import get_session, Evaluation

st.title("🕒 Evaluation History")
st.markdown("Review your past evaluations, track your progress, and export data.")

# Utility to convert SQLAlchemy model instances to dict
def model_to_dict(obj):
    return {c.key: getattr(obj, c.key) for c in class_mapper(obj.__class__).columns}

# Fetch data
db = get_session()
evaluations = db.query(Evaluation).order_by(Evaluation.created_at.desc()).all()
db.close()

if not evaluations:
    st.info("No evaluations found. Go to Writing or Speaking to create one!")
else:
    df = pd.DataFrame([model_to_dict(e) for e in evaluations])

    # --- Summary strip ---
    s1, s2, s3 = st.columns(3)
    with s1:
        st.metric("📚 Total Evaluations", len(df))
    with s2:
        st.metric("✍️ Writing", int((df['type'] == 'writing').sum()))
    with s3:
        st.metric("🎙️ Speaking", int((df['type'] == 'speaking').sum()))

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Filter & Search ---
    with st.container(border=True):
        st.markdown("#### 🔎 Filter & Search")
        col1, col2 = st.columns(2)
        with col1:
            type_filter = st.selectbox("Type", ["All", "writing", "speaking"])
        with col2:
            search_query = st.text_input("Search (by text/transcript or feedback)")

        filtered_df = df.copy()

        if type_filter != "All":
            filtered_df = filtered_df[filtered_df['type'] == type_filter]

        if search_query:
            search_query = search_query.lower()
            # Ensure string type before checking for 'str.contains' and fill NAs
            mask = (
                filtered_df['input_text'].astype(str).str.lower().str.contains(search_query) |
                filtered_df['transcript'].astype(str).str.lower().str.contains(search_query) |
                filtered_df['feedback'].astype(str).str.lower().str.contains(search_query)
            )
            filtered_df = filtered_df[mask]

        st.caption(f"**Found {len(filtered_df)} records**")

        # Display Dataframe
        display_cols = ['id', 'type', 'created_at', 'overall_score', 'grammar_score', 'vocabulary_score', 'coherence_score', 'fluency_score']
        st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)

        # Export CSV
        csv_data = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export to CSV",
            data=csv_data,
            file_name='evaluations_history.csv',
            mime='text/csv',
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- Details ---
    with st.container(border=True):
        st.markdown("#### 📄 View Details or Delete")

        # Selection for detailed view
        selected_id = st.selectbox("Select an evaluation ID to view details or delete", filtered_df['id'].tolist(), index=None)

        if selected_id:
            record = filtered_df[filtered_df['id'] == selected_id].iloc[0]

            st.markdown(f"##### Evaluation #{record['id']} ({record['type']})")
            st.caption(f"**Date:** {record['created_at']}")

            if record['type'] == 'writing':
                st.markdown("**Original Text:**")
                st.write(record['input_text'])
            else:
                st.markdown("**Transcript:**")
                st.write(record['transcript'])
                if pd.notna(record['audio_path']):
                    st.audio(record['audio_path'])

            st.markdown("**Feedback:**")
            st.info(record['feedback'])

            if st.button("🗑️ Delete Record"):
                try:
                    db = get_session()
                    record_to_delete = db.query(Evaluation).filter(Evaluation.id == selected_id).first()
                    if record_to_delete:
                        db.delete(record_to_delete)
                        db.commit()
                        st.success("Record deleted successfully! Please refresh the page.")
                        # Optionally handle rerun
                        # st.rerun()
                    db.close()
                except Exception as e:
                    st.error(f"Failed to delete record: {e}")
