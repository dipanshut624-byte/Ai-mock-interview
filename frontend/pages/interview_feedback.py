import streamlit as st
import requests

API_BASE_URL = 'http://localhost:8000/api'

st.set_page_config(page_title="Interview Feedback", page_icon="📊", layout="wide")

st.header("📊 Interview Feedback")

if 'current_interview' not in st.session_state or not st.session_state.current_interview:
    st.error("No interview data available.")
    st.stop()

interview = st.session_state.current_interview
interview_id = interview['id']

# Fetch latest interview data
response = requests.get(f"{API_BASE_URL}/interviews/{interview_id}/")

if response.status_code == 200:
    interview = response.json()
    
    # Overall score
    st.markdown("## Overall Performance")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Overall Score",
            f"{interview.get('overall_score', 0):.1f}",
            f"/100"
        )
    
    with col2:
        duration = interview.get('duration_seconds', 0)
        minutes = duration // 60
        st.metric("Duration", f"{minutes} min")
    
    with col3:
        questions_count = len(interview.get('questions', []))
        st.metric("Questions", questions_count)
    
    with col4:
        responses_count = len(interview.get('responses', []))
        st.metric("Answered", responses_count)
    
    st.divider()
    
    # Detailed feedback
    if interview.get('feedback_report'):
        st.markdown("## Comprehensive Feedback")
        st.markdown(interview.get('feedback_report', ''))
    
    st.divider()
    
    # Individual responses
    st.markdown("## Response Details")
    
    responses = interview.get('responses', [])
    
    for idx, response_data in enumerate(responses, 1):
        with st.expander(
            f"Q{idx}: {interview['questions'][idx-1]['question_text'][:50]}...",
            expanded=False
        ):
            st.markdown("### Your Answer")
            st.write(response_data.get('response_text', 'No text provided'))
            
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("Overall", f"{response_data.get('overall_score', 0):.0f}/100")
            with col2:
                st.metric("Relevance", f"{response_data.get('relevance_score', 0):.0f}/10")
            with col3:
                st.metric("Complete", f"{response_data.get('completeness_score', 0):.0f}/10")
            with col4:
                st.metric("Technical", f"{response_data.get('technical_depth_score', 0):.0f}/10")
            with col5:
                st.metric("Comm.", f"{response_data.get('communication_score', 0):.0f}/10")
            
            st.markdown("### Feedback")
            st.info(response_data.get('feedback', 'No feedback available'))
            
            col1, col2 = st.columns(2)
            
            with col1:
                strengths = response_data.get('strengths', [])
                if strengths:
                    st.markdown("**Strengths:**")
                    for strength in strengths:
                        st.write(f"✅ {strength}")
            
            with col2:
                improvements = response_data.get('areas_for_improvement', [])
                if improvements:
                    st.markdown("**Areas to Improve:**")
                    for improvement in improvements:
                        st.write(f"🎯 {improvement}")
    
    st.divider()
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Start New Interview"):
            st.session_state.current_interview = None
            st.switch_page("pages/start_interview.py")
    
    with col2:
        if st.button("Download Report"):
            st.info("📥 Download feature coming soon!")
    
    with col3:
        if st.button("Go to Home"):
            st.switch_page("app.py")

else:
    st.error("Error fetching interview details")
