import streamlit as st
import requests

API_BASE_URL = 'http://localhost:8000/api'

st.set_page_config(page_title="Interview Details", page_icon="📋", layout="wide")

st.header("📋 Interview Details")

if 'current_interview' not in st.session_state or not st.session_state.current_interview:
    st.error("No interview selected.")
    st.stop()

interview_id = st.session_state.current_interview['id']

# Fetch full interview data
response = requests.get(f"{API_BASE_URL}/interviews/{interview_id}/")

if response.status_code == 200:
    interview = response.json()
    
    # Header info
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Job Role", interview.get('job_role', {}).get('name', 'N/A') if interview.get('job_role') else 'N/A')
    
    with col2:
        st.metric("Status", interview.get('status', '').title())
    
    with col3:
        st.metric("Overall Score", f"{interview.get('overall_score', 0):.1f}/100")
    
    st.divider()
    
    # Questions and responses
    st.markdown("## Questions & Answers")
    
    questions = interview.get('questions', [])
    responses = interview.get('responses', [])
    
    if not questions:
        st.info("No questions in this interview yet.")
    else:
        for idx, question in enumerate(questions, 1):
            with st.expander(f"Question {idx}: {question['question_text']}", expanded=False):
                st.markdown(f"**Q: {question['question_text']}**")
                
                # Find corresponding response
                matching_response = next(
                    (r for r in responses if r['question'] == question['id']),
                    None
                )
                
                if matching_response:
                    st.markdown("**Your Answer:**")
                    st.write(matching_response['response_text'])
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Score", f"{matching_response['overall_score']:.0f}/100")
                    with col2:
                        st.metric("Relevance", f"{matching_response['relevance_score']:.0f}/10")
                    with col3:
                        st.metric("Technical Depth", f"{matching_response['technical_depth_score']:.0f}/10")
                    
                    if matching_response.get('feedback'):
                        st.markdown("**Feedback:**")
                        st.info(matching_response['feedback'])
                else:
                    st.warning("No response submitted for this question")
    
    st.divider()
    
    # Comprehensive feedback
    if interview.get('feedback_report'):
        st.markdown("## Comprehensive Report")
        st.markdown(interview['feedback_report'])
    
    st.divider()
    
    # Navigation
    if st.button("Back to Interview History"):
        st.switch_page("app.py")

else:
    st.error("Error fetching interview details")
