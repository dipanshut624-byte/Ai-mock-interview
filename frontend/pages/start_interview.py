import streamlit as st
import requests

API_BASE_URL = 'http://localhost:8000/api'

st.set_page_config(page_title="Start Interview", page_icon="🎤", layout="wide")

st.header("🎤 Start Interview")

# Interview mode selection
st.markdown("### Select Interview Mode")

interview_mode = st.radio(
    "Choose how you want to be interviewed:",
    options=["Standard Interview", "Agent Interview (Conversational AI)", "Video Interview (FAANG-style)"],
    help="Standard: Answer pre-generated questions. Agent: Natural conversation. Video: Real one-on-one with camera (like FAANG companies)."
)

try:
    # Get available job roles
    response = requests.get(f"{API_BASE_URL}/job-roles/")
    job_roles = response.json().get('results', [])
    
    if not job_roles:
        st.error("No job roles available. Please check back later.")
        st.stop()
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_job = st.selectbox(
            "Select Job Role:",
            options=job_roles,
            format_func=lambda x: x['name'],
            key="job_select"
        )
    
    with col2:
        if interview_mode == "Standard Interview":
            num_questions = st.slider(
                "Number of Questions:",
                min_value=3,
                max_value=10,
                value=5,
                key="num_q"
            )
        else:
            st.info("Agent will adapt question count based on conversation.")
    
    # Check if resume exists in session
    if 'current_resume' not in st.session_state:
        st.warning("⚠️ Please upload your resume first.")
        if st.button("Go to Upload Resume"):
            st.switch_page("app.py")
        st.stop()
    
    if st.button("Start Interview Session", type="primary"):
        with st.spinner("Starting interview..."):
            interview_data = {
                'job_role_id': selected_job['id'],
                'resume_id': st.session_state.current_resume['id']
            }
            
            # Create interview
            create_response = requests.post(
                f"{API_BASE_URL}/interviews/",
                json=interview_data
            )
            
            if create_response.status_code == 201:
                interview = create_response.json()
                st.session_state.interview_id = interview['id']
                st.session_state.interview_mode = interview_mode
                
                if interview_mode == "Standard Interview":
                    # Start standard interview with pre-generated questions
                    start_response = requests.post(
                        f"{API_BASE_URL}/interviews/{interview['id']}/start_interview/",
                        json={'num_questions': num_questions}
                    )
                    
                    if start_response.status_code == 200:
                        st.session_state.current_interview = start_response.json()
                        st.success("✅ Interview started successfully!")
                        st.switch_page("pages/conduct_interview.py")
                    else:
                        error_msg = start_response.json().get('error', 'Unknown error')
                        st.error(f"Error starting interview: {error_msg}")
                
                elif interview_mode == "Agent Interview (Conversational AI)":
                    st.session_state.interview_id = interview['id']
                    st.session_state.conversation_history = []
                    st.session_state.question_index = 0
                    st.session_state.job_role = selected_job['name']
                    st.success("✅ Agent interview starting...")
                    st.switch_page("pages/agent_interview.py")
                
                else:  # Video Interview
                    st.session_state.interview_id = interview['id']
                    st.session_state.video_conversation_history = []
                    st.session_state.job_role = selected_job['name']
                    st.success("✅ Video interview starting...")
                    st.switch_page("pages/video_interview.py")
            else:
                error_msg = create_response.json().get('error', 'Unknown error')
                st.error(f"Error creating interview: {error_msg}")

except Exception as e:
    st.error(f"Error: {str(e)}")
