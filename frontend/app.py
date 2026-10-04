import streamlit as st
import requests
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000/api')

# Page configuration
st.set_page_config(
    page_title="AI Mock Interview System",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
    }
    .score-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .feedback-box {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    """Main app entry point."""
    st.markdown("""
        <div class="header">
            <h1>🎤 AI-Powered Mock Interview System</h1>
            <p>Practice interviews with AI feedback and improve your performance</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Session state initialization
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    if 'current_interview' not in st.session_state:
        st.session_state.current_interview = None
    if 'resume_uploaded' not in st.session_state:
        st.session_state.resume_uploaded = False
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page:",
        ["Home", "Upload Resume", "Browse Jobs", "Start Interview", "Interview History", "Practice Tips"]
    )
    
    if page == "Home":
        show_home()
    elif page == "Upload Resume":
        show_upload_resume()
    elif page == "Browse Jobs":
        show_browse_jobs()
    elif page == "Start Interview":
        show_start_interview()
    elif page == "Interview History":
        show_interview_history()
    elif page == "Practice Tips":
        show_practice_tips()


def show_home():
    """Display home page."""
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("## Welcome to Your Interview Practice Platform")
        st.write("""
        Prepare for your next job interview with our AI-powered mock interview system!
        
        **Key Features:**
        - 📄 Upload your resume for personalized questions
        - 🎯 Choose target job roles
        - 🤖 AI-generated questions based on your profile
        - 📊 Real-time scoring and feedback
        - 🎙️ Support for text and audio responses
        - 📈 Track your progress over time
        """)
    
    with col2:
        st.markdown("## Getting Started")
        st.info("""
        **Step 1:** Upload your resume
        
        **Step 2:** Browse available job roles
        
        **Step 3:** Start an interview session
        
        **Step 4:** Answer generated questions
        
        **Step 5:** Review detailed feedback
        """)
    
    st.markdown("---")
    st.markdown("## Why Practice Interviews Matter?")
    st.write("""
    - Gain confidence in real interview scenarios
    - Get instant, AI-powered feedback on your responses
    - Identify areas for improvement
    - Practice different job roles and scenarios
    - Build a history of your performance progress
    """)


def show_upload_resume():
    """Display resume upload page."""
    st.header("📄 Upload Your Resume")
    
    st.write("Upload your resume to get started. Our AI will analyze your skills and experience.")
    
    uploaded_file = st.file_uploader(
        "Choose your resume (PDF)",
        type=['pdf', 'txt'],
        help="Upload a PDF or text file of your resume"
    )
    
    if uploaded_file is not None:
        try:
            with st.spinner("Processing your resume..."):
                files = {'file': uploaded_file}
                response = requests.post(
                    f"{API_BASE_URL}/resumes/",
                    files=files
                )
                
                if response.status_code == 201:
                    resume_data = response.json()
                    st.session_state.resume_uploaded = True
                    st.session_state.current_resume = resume_data
                    
                    st.success("✅ Resume uploaded successfully!")
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Skills Found", len(resume_data.get('skills', [])))
                    
                    with col2:
                        st.metric("Years of Experience", resume_data.get('experience_years', 0))
                    
                    with col3:
                        st.metric("Resume ID", resume_data.get('id', 'N/A'))
                    
                    st.write("**Skills Identified:**")
                    skills = resume_data.get('skills', [])
                    shortlist_data = None
                    if skills:
                        skill_cols = st.columns(3)
                        for idx, skill in enumerate(skills):
                            with skill_cols[idx % 3]:
                                st.markdown(f"- {skill}")

                    with st.spinner("Generating shortlist insights..."):
                        shortlist_response = requests.get(
                            f"{API_BASE_URL}/resumes/{resume_data.get('id')}/shortlist/"
                        )
                        if shortlist_response.status_code == 200:
                            shortlist_data = shortlist_response.json()

                    if shortlist_data:
                        st.markdown("## 🔍 Shortlist Insights")
                        st.markdown(f"**Fit Summary:** {shortlist_data.get('fit_summary', '')}")

                        recommended_roles = shortlist_data.get('recommended_roles', [])
                        if recommended_roles:
                            st.markdown("**Recommended Roles:**")
                            for role in recommended_roles:
                                st.markdown(f"- {role}")

                        strengths = shortlist_data.get('key_strengths', [])
                        if strengths:
                            st.markdown("**Key Strengths:**")
                            for strength in strengths:
                                st.markdown(f"- {strength}")

                        gaps = shortlist_data.get('skill_gaps', [])
                        if gaps:
                            st.markdown("**Skill Gaps:**")
                            for gap in gaps:
                                st.markdown(f"- {gap}")

                        next_steps = shortlist_data.get('recommended_next_steps', [])
                        if next_steps:
                            st.markdown("**Recommended Next Steps:**")
                            for step in next_steps:
                                st.markdown(f"- {step}")

                    st.write("**Contact Information:**")
                    contact_info = resume_data.get('contact_info', {})
                    for key, value in contact_info.items():
                        st.write(f"- **{key.title()}:** {value}")
                
                else:
                    st.error(f"Error uploading resume: {response.json().get('error', 'Unknown error')}")
        
        except Exception as e:
            st.error(f"Error processing resume: {str(e)}")


def show_browse_jobs():
    """Display job roles browsing page."""
    st.header("🎯 Browse Job Roles")
    
    try:
        response = requests.get(f"{API_BASE_URL}/job-roles/")
        
        if response.status_code == 200:
            job_roles = response.json().get('results', [])
            
            if not job_roles:
                st.info("No job roles available. Administrators will add them soon.")
            else:
                # Filter options
                col1, col2 = st.columns(2)
                with col1:
                    experience_filter = st.selectbox(
                        "Filter by experience level:",
                        ["All", "Junior", "Mid-Level", "Senior", "Lead"],
                        key="exp_filter"
                    )
                
                with col2:
                    search_term = st.text_input("Search job roles:")
                
                # Filter jobs
                filtered_jobs = [
                    job for job in job_roles
                    if (experience_filter == "All" or job.get('experience_level', '').lower() == experience_filter.lower())
                    and (search_term.lower() in job.get('name', '').lower() or 
                         search_term.lower() in job.get('description', '').lower())
                ]
                
                for job in filtered_jobs:
                    with st.container():
                        col1, col2 = st.columns([4, 1]
                        )
                        with col1:
                            st.subheader(job.get('name', 'N/A'))
                            st.write(job.get('description', ''))
                            
                            experience = job.get('experience_level', '').title()
                            required_skills = job.get('required_skills', [])
                            
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.write(f"**Level:** {experience}")
                            with col_b:
                                st.write(f"**Skills:** {', '.join(required_skills) if required_skills else 'N/A'}")
                        
                        with col2:
                            if st.button("Start Interview", key=f"job_{job['id']}"):
                                st.session_state.selected_job = job
                                st.switch_page("pages/start_interview.py")
                        
                        st.divider()
        else:
            st.error("Unable to fetch job roles")
    
    except Exception as e:
        st.error(f"Error fetching job roles: {str(e)}")


def show_start_interview():
    """Display start interview page."""
    st.header("🎤 Start Interview")
    
    if not st.session_state.resume_uploaded:
        st.warning("⚠️ Please upload your resume first to start an interview.")
        st.button("Go to Upload Resume →")
        return
    
    try:
        # Get available job roles
        response = requests.get(f"{API_BASE_URL}/job-roles/")
        job_roles = response.json().get('results', [])
        
        if not job_roles:
            st.error("No job roles available")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            selected_job = st.selectbox(
                "Select Job Role:",
                options=job_roles,
                format_func=lambda x: x['name']
            )
        
        with col2:
            num_questions = st.slider(
                "Number of Questions:",
                min_value=3,
                max_value=10,
                value=5
            )
        
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
                    st.session_state.current_interview = interview
                    
                    # Start interview and generate questions
                    start_response = requests.post(
                        f"{API_BASE_URL}/interviews/{interview['id']}/start_interview/",
                        json={'num_questions': num_questions}
                    )
                    
                    if start_response.status_code == 200:
                        st.success("✅ Interview started successfully!")
                        st.session_state.current_interview = start_response.json()
                        st.switch_page("pages/conduct_interview.py")
                    else:
                        st.error("Error starting interview")
                else:
                    st.error("Error creating interview session")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")


def show_interview_history():
    """Display interview history page."""
    st.header("📈 Interview History")
    
    try:
        response = requests.get(f"{API_BASE_URL}/interviews/")
        
        if response.status_code == 200:
            interviews = response.json().get('results', [])
            
            if not interviews:
                st.info("No interviews yet. Start your first interview!")
            else:
                # Display statistics
                col1, col2, col3, col4 = st.columns(4)
                
                completed = [i for i in interviews if i['status'] == 'completed']
                
                with col1:
                    st.metric("Total Interviews", len(interviews))
                with col2:
                    st.metric("Completed", len(completed))
                with col3:
                    avg_score = sum(i['overall_score'] for i in completed) / len(completed) if completed else 0
                    st.metric("Average Score", f"{avg_score:.1f}/100")
                with col4:
                    in_progress = [i for i in interviews if i['status'] == 'in_progress']
                    st.metric("In Progress", len(in_progress))
                
                st.divider()
                
                # Interview list
                st.subheader("Your Interviews")
                
                for interview in sorted(interviews, key=lambda x: x['created_at'], reverse=True):
                    with st.container():
                        col1, col2, col3 = st.columns([2, 1, 1])
                        
                        with col1:
                            job_role = interview.get('job_role_name', 'Unknown')
                            created_date = interview.get('created_at', '').split('T')[0]
                            st.write(f"**{job_role}** - {created_date}")
                            
                            status_color = {
                                'completed': '🟢',
                                'in_progress': '🟡',
                                'scheduled': '🔵',
                                'paused': '⚫'
                            }
                            status_emoji = status_color.get(interview.get('status', ''), '❓')
                            st.write(f"{status_emoji} {interview.get('status', '').title()}")
                        
                        with col2:
                            score = interview.get('overall_score', 0)
                            st.write(f"**Score:** {score:.1f}/100")
                        
                        with col3:
                            if st.button("View Details", key=f"interview_{interview['id']}"):
                                st.session_state.current_interview = interview
                                st.switch_page("pages/interview_details.py")
                        
                        st.divider()
        else:
            st.error("Unable to fetch interview history")
    
    except Exception as e:
        st.error(f"Error fetching interview history: {str(e)}")


def show_practice_tips():
    """Display practice tips page."""
    st.header("💡 Interview Preparation Tips")
    
    st.markdown("""
    ### Technical Interview Tips
    
    1. **Understand the Question**
       - Take a moment to understand what's being asked
       - Ask clarifying questions if needed
       - Structure your answer before speaking
    
    2. **Provide Context**
       - Explain your approach and reasoning
       - Discuss trade-offs and alternatives
       - Share relevant examples from your experience
    
    3. **Demonstrate Problem-Solving**
       - Break down complex problems
       - Show your thinking process
       - Discuss edge cases and improvements
    
    ### Behavioral Interview Tips
    
    1. **Use the STAR Method**
       - **S**ituation: Set the context
       - **T**ask: Explain what you needed to do
       - **A**ction: Describe what you did
       - **R**esult: Share the outcome and lessons
    
    2. **Be Specific**
       - Use concrete examples
       - Include metrics and achievements
       - Avoid vague generalizations
    
    3. **Show Growth**
       - Discuss what you learned
       - Share how you improved
       - Demonstrate self-awareness
    
    ### General Tips
    
    - 🎤 **Speak Clearly:** Enunciate and speak at a reasonable pace
    - 📝 **Be Concise:** Avoid rambling or going off-topic
    - 🧠 **Stay Calm:** It's okay to take a moment to think
    - 👂 **Listen:** Pay attention to follow-up questions
    - 📊 **Practice:** The more you practice, the better you'll perform
    
    ### Common Mistakes to Avoid
    
    ❌ Memorizing answers word-for-word
    ❌ Talking too much without letting the interviewer ask questions
    ❌ Being defensive about past experiences
    ❌ Not asking clarifying questions
    ❌ Focusing only on technical skills (ignore soft skills)
    """)


if __name__ == "__main__":
    main()
