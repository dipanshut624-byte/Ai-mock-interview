"""Agent-based interview page with conversational AI interviewer."""

import streamlit as st
import requests
import json
from datetime import datetime

API_BASE_URL = "http://localhost:8000/api"

st.set_page_config(page_title="Agent Interview", page_icon="🤖", layout="wide")

st.header("🤖 AI Agent Interview")
st.write("Conduct a natural interview with your AI interviewer. Answer conversationally and receive real-time feedback.")

# Check if interview exists
if 'interview_id' not in st.session_state:
    st.warning("⚠️ No active interview. Please create an interview first.")
    st.stop()

interview_id = st.session_state.get('interview_id')
conversation_history = st.session_state.get('conversation_history', [])
question_index = st.session_state.get('question_index', 0)
job_role = st.session_state.get('job_role', '')

# Initialize interview if not started
if 'agent_started' not in st.session_state:
    st.session_state.agent_started = False

if not st.session_state.agent_started:
    with st.spinner("Starting AI interview..."):
        response = requests.post(
            f"{API_BASE_URL}/interviews/{interview_id}/start_agent_interview/",
            json={}
        )
        
        if response.status_code == 200:
            data = response.json()
            st.session_state.agent_started = True
            st.session_state.conversation_history = data.get('conversation_history', [])
            st.session_state.question_index = data.get('question_number', 1)
            st.session_state.job_role = data.get('job_role', '')
            conversation_history = st.session_state.conversation_history
        else:
            st.error(f"Error starting interview: {response.json().get('error', 'Unknown error')}")
            st.stop()

# Display conversation history
st.markdown("### Interview Conversation")

conversation_container = st.container()
with conversation_container:
    for msg in conversation_history:
        if msg.get("role") == "assistant":
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(msg.get("content", ""))
        elif msg.get("role") == "user":
            with st.chat_message("user", avatar="👤"):
                st.markdown(msg.get("content", ""))

# Input area for candidate response
st.markdown("---")
st.markdown("### Your Response")

candidate_response = st.text_area(
    "Type your answer to the AI interviewer's question:",
    placeholder="Share your thoughts, experiences, and expertise...",
    height=150,
    key="response_input"
)

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    if st.button("💬 Submit Response", type="primary"):
        if not candidate_response.strip():
            st.error("Please provide a response before submitting.")
        else:
            with st.spinner("AI interviewer evaluating your response..."):
                response = requests.post(
                    f"{API_BASE_URL}/interviews/{interview_id}/agent_chat/",
                    json={
                        'response': candidate_response,
                        'conversation_history': st.session_state.conversation_history,
                        'question_index': st.session_state.question_index
                    }
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Update session state
                    st.session_state.conversation_history = data.get('conversation_history', [])
                    st.session_state.question_index = data.get('question_number', st.session_state.question_index + 1)
                    
                    # Show evaluation feedback
                    st.success("✅ Response recorded!")
                    
                    if data.get('evaluation'):
                        eval_data = data.get('evaluation')
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Score", f"{eval_data.get('score', 0)}/10")
                        with col2:
                            st.metric("Question #", data.get('question_number', ''))
                        
                        if eval_data.get('strengths'):
                            st.markdown("**Strengths:**")
                            for strength in eval_data.get('strengths', []):
                                st.markdown(f"✓ {strength}")
                        
                        if eval_data.get('gaps'):
                            st.markdown("**Areas to develop:**")
                            for gap in eval_data.get('gaps', []):
                                st.markdown(f"• {gap}")
                    
                    if data.get('feedback'):
                        st.info(f"**Feedback:** {data.get('feedback')}")
                    
                    st.rerun()
                else:
                    st.error(f"Error: {response.json().get('error', 'Unknown error')}")

with col2:
    if st.button("⏸️ Pause"):
        st.session_state.paused = True
        st.success("Interview paused.")

with col3:
    if st.button("🏁 End"):
        st.session_state.interview_complete = True
        st.success("Interview ended. Generating report...")
        # Could trigger final report generation here
        st.switch_page("pages/interview_details.py")

# Sidebar with interview stats
with st.sidebar:
    st.markdown("### Interview Stats")
    st.metric("Job Role", job_role)
    st.metric("Question #", question_index)
    st.metric("Started At", st.session_state.get('interview_start_time', 'Just now'))
    
    if st.button("📊 View Detailed Stats"):
        st.switch_page("pages/interview_details.py")
