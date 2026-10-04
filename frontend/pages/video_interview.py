"""Real one-on-one video interview with AI agent (FAANG-style)."""

import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import requests
from datetime import datetime

API_BASE_URL = "http://localhost:8000/api"

st.set_page_config(
    page_title="Video Interview",
    page_icon="📹",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        .interview-container {
            display: flex;
            gap: 20px;
            margin-top: 20px;
        }
        .video-section {
            flex: 1;
            border: 2px solid #333;
            border-radius: 10px;
            padding: 20px;
            background: #1a1a1a;
        }
        .question-section {
            flex: 1;
            border: 2px solid #0066cc;
            border-radius: 10px;
            padding: 20px;
            background: #f0f8ff;
        }
        .feedback-box {
            background: #e8f5e9;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            border-left: 4px solid #4caf50;
        }
        .timer {
            font-size: 24px;
            font-weight: bold;
            text-align: center;
            margin: 10px 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

if 'interview_id' not in st.session_state:
    st.warning("⚠️ No active interview. Please create a video interview first.")
    if st.button("← Back to Start Interview"):
        st.switch_page("pages/start_interview.py")
    st.stop()

interview_id = st.session_state.get('interview_id')
job_role = st.session_state.get('job_role', '')

if 'video_conversation_history' not in st.session_state:
    st.session_state.video_conversation_history = []
if 'video_interview_started' not in st.session_state:
    st.session_state.video_interview_started = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = ""
if 'interview_start_time' not in st.session_state:
    st.session_state.interview_start_time = datetime.now()
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0
if 'messages' not in st.session_state:
    st.session_state.messages = []

st.markdown("# 📹 Video Interview Session")
st.markdown(f"**Position:** {job_role}")

if not st.session_state.video_interview_started:
    st.markdown("### 👋 Welcome to Your Video Interview")
    st.markdown(
        """
        This is a real one-on-one interview experience designed
        to simulate actual FAANG company interviews.

        **What to expect:**
        - 🎥 Your camera will be active throughout
        - 🤖 AI agent will ask contextual questions
        - 📊 Real-time feedback
        - ⏱️ Interview timer

        Click **Start Interview** when ready!
        """
    )

    if st.button("▶️ Start Interview", type="primary"):
        with st.spinner("Starting AI interview..."):
            response = requests.post(
                f"{API_BASE_URL}/interviews/{interview_id}/start_agent_interview/",
                json={},
            )

            if response.status_code == 200:
                data = response.json()
                st.session_state.video_interview_started = True
                st.session_state.current_question = data.get('first_question', 'Tell me about yourself.')
                st.session_state.question_count = 1
                st.session_state.messages = [{
                    "role": "assistant",
                    "content": st.session_state.current_question,
                }]
                st.session_state.video_conversation_history = data.get('conversation_history', [])
                st.success("✅ AI interview started successfully!")
                st.rerun()
            else:
                error_msg = response.json().get('error', 'Unknown error')
                st.error(f"Error starting interview: {error_msg}")
    st.stop()

left_col, right_col = st.columns([1.5, 1])

with left_col:
    st.markdown("## Your Video Feed")
    rtc_configuration = RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )

    webrtc_streamer(
        key="interview-video",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=rtc_configuration,
        media_stream_constraints={"audio": True, "video": True},
        async_processing=True,
    )

with right_col:
    st.markdown("### 📋 Current Question")
    st.info(f"**Q{st.session_state.question_count}:** {st.session_state.current_question}")

    st.markdown("## 🤖 AI Interview Chat")
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Type your answer here...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("AI Interviewer is thinking..."):
            response = requests.post(
                f"{API_BASE_URL}/interviews/{interview_id}/agent_chat/",
                json={
                    "response": prompt,
                    "conversation_history": st.session_state.messages,
                    "question_index": st.session_state.question_count,
                },
            )

            if response.status_code == 200:
                data = response.json()
                ai_reply = data.get("next_question", "Tell me more about yourself.")
                st.session_state.current_question = ai_reply
                st.session_state.question_count += 1
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})

                if data.get("evaluation"):
                    eval_data = data.get("evaluation")
                    st.markdown("### 📊 AI Feedback")
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.metric("Score", f"{eval_data.get('score', 0)}/10")
                    with col2:
                        st.metric("Question", st.session_state.question_count)
                    with col3:
                        elapsed = (datetime.now() - st.session_state.interview_start_time).total_seconds() / 60
                        st.metric("Time", f"{elapsed:.1f}m")

                    if eval_data.get("strengths"):
                        st.markdown("#### ✅ Strengths")
                        for strength in eval_data.get("strengths", []):
                            st.markdown(f"- {strength}")

                    if eval_data.get("gaps"):
                        st.markdown("#### ⚠️ Improvements")
                        for gap in eval_data.get("gaps", []):
                            st.markdown(f"- {gap}")

                st.rerun()
            else:
                st.error("Backend AI failed. Please try again.")

    if st.button("🏁 End Interview"):
        st.session_state.video_interview_started = False
        st.success("Interview ended.")
        st.switch_page("pages/start_interview.py")

    with st.expander("📜 Interview History"):
        for msg in st.session_state.messages:
            role = msg.get("role")
            content = msg.get("content")
            if role == "user":
                st.markdown(f"**You:** {content}")
            elif role == "assistant":
                st.markdown(f"**AI:** {content}")
