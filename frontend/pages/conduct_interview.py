import streamlit as st
import requests
import json
from datetime import datetime

API_BASE_URL = 'http://localhost:8000/api'

st.set_page_config(page_title="Conduct Interview", page_icon="🎤", layout="wide")

st.header("🎤 Interview in Progress")

if 'current_interview' not in st.session_state or not st.session_state.current_interview:
    st.error("No active interview. Please start an interview first.")
    st.stop()

interview = st.session_state.current_interview
interview_id = interview['id']

# Get current question
response = requests.get(f"{API_BASE_URL}/interviews/{interview_id}/get_next_question/")

if response.status_code == 200:
    question_data = response.json()
    
    if 'message' in question_data:
        st.success("✅ All questions answered! Completing interview...")
        
        # Complete interview
        complete_response = requests.post(
            f"{API_BASE_URL}/interviews/{interview_id}/complete_interview/"
        )
        
        if complete_response.status_code == 200:
            st.session_state.current_interview = complete_response.json()
            st.success("Interview completed successfully!")
            
            if st.button("View Your Feedback"):
                st.switch_page("pages/interview_feedback.py")
        st.stop()
    
    # Display question
    question = question_data.get('question_text', '')
    question_number = question_data.get('question_number', 1)
    question_id = question_data.get('id', '')
    
    st.markdown(f"### Question {question_number}")
    st.markdown(f"**{question}**")
    
    # Get total questions
    total_questions = len(interview.get('questions', []))
    
    # Progress bar
    st.progress((question_number - 1) / total_questions)
    st.write(f"Question {question_number} of {total_questions}")
    
    st.divider()
    
    # Response input
    st.subheader("Your Answer")
    
    response_method = st.radio(
        "Choose response method:",
        ["Text", "Audio"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    if response_method == "Text":
        answer_text = st.text_area(
            "Type your answer here:",
            height=150,
            placeholder="Share your thoughts, experience, and approach..."
        )
        
        if st.button("Submit Answer", type="primary", key="submit_text"):
            if not answer_text.strip():
                st.error("Please provide an answer before submitting.")
            else:
                with st.spinner("Evaluating your response..."):
                    submit_response = requests.post(
                        f"{API_BASE_URL}/interviews/{interview_id}/submit_response/",
                        json={
                            'question_id': question_id,
                            'response_text': answer_text,
                            'delivery_method': 'text'
                        }
                    )
                    
                    if submit_response.status_code == 200:
                        response_data = submit_response.json()
                        
                        # Display immediate feedback
                        st.success("✅ Response evaluated!")
                        
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric(
                                "Overall Score",
                                f"{response_data.get('overall_score', 0):.0f}/100"
                            )
                        
                        with col2:
                            relevance = response_data.get('relevance_score', 0)
                            st.metric("Relevance", f"{relevance:.0f}/10")
                        
                        with col3:
                            depth = response_data.get('technical_depth_score', 0)
                            st.metric("Technical Depth", f"{depth:.0f}/10")
                        
                        st.divider()
                        
                        # Feedback
                        if response_data.get('feedback'):
                            st.markdown("### AI Feedback")
                            st.info(response_data.get('feedback', ''))
                        
                        # Strengths and areas for improvement
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            strengths = response_data.get('strengths', [])
                            if strengths:
                                st.markdown("### ✅ Strengths")
                                for strength in strengths:
                                    st.write(f"- {strength}")
                        
                        with col2:
                            improvements = response_data.get('areas_for_improvement', [])
                            if improvements:
                                st.markdown("### 🎯 Areas for Improvement")
                                for improvement in improvements:
                                    st.write(f"- {improvement}")
                        
                        if response_data.get('follow_up_question'):
                            st.markdown("### Follow-up Question")
                            st.write(response_data.get('follow_up_question'))
                        
                        st.divider()
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Next Question", type="primary", key="next_q"):
                                st.rerun()
                        with col2:
                            if st.button("End Interview", key="end_int"):
                                st.switch_page("pages/interview_feedback.py")
                    else:
                        st.error("Error submitting response. Please try again.")
    
    else:  # Audio mode
        st.info("🎙️ Audio recording feature coming soon. For now, please use text responses.")

else:
    st.error("Error fetching question")
