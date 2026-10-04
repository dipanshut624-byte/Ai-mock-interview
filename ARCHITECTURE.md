# System Architecture

## High-Level Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER (Streamlit)                   │
├─────────────────────────────────────────────────────────────────┤
│  Home │ Upload Resume │ Browse Jobs │ Start Interview │ History │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    HTTP REST API
                    (localhost:8000)
                           │
┌──────────────────────────┴──────────────────────────────────────┐
│                    BACKEND LAYER (Django)                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  ┌─ API Views                                                    │
│  │  ├─ JobRoleViewSet                                           │
│  │  ├─ ResumeViewSet                                            │
│  │  └─ InterviewViewSet                                         │
│  │                                                               │
│  ├─ Core Services                                               │
│  │  ├─ AIService (OpenAI Integration)                           │
│  │  │  ├─ generate_questions()                                  │
│  │  │  ├─ evaluate_response()                                   │
│  │  │  └─ generate_feedback_report()                            │
│  │  │                                                            │
│  │  └─ ResumeParser                                             │
│  │     ├─ extract_text_from_pdf()                               │
│  │     ├─ extract_skills()                                      │
│  │     └─ extract_experience_years()                            │
│  │                                                               │
│  └─ Database Models                                             │
│     ├─ JobRole                                                  │
│     ├─ Resume                                                   │
│     ├─ Interview                                                │
│     ├─ InterviewQuestion                                        │
│     ├─ InterviewResponse                                        │
│     └─ InterviewFeedback                                        │
│                                                                   │
└──────────────┬──────────────────────────────────────────────────┘
               │
┌──────────────┴──────────────────────────────────────────────────┐
│              EXTERNAL SERVICES & DATA LAYER                      │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │ OpenAI GPT   │  │   SQLite     │  │ File Storage │          │
│  │  API         │  │  Database    │  │  (Resumes)   │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

## Component Details

### Frontend (Streamlit)
- **app.py**: Main application with navigation
- **pages/**: Multi-page sections
  - `conduct_interview.py`: Interview Q&A interface
  - `interview_feedback.py`: Results and feedback display
  - `interview_details.py`: Historical interview details
  - `start_interview.py`: Interview setup wizard

### Backend (Django)
- **Models**: Data structures for interviews, responses, etc.
- **ViewSets**: REST API endpoints
- **Serializers**: Data validation and transformation
- **Services**: Business logic
  - **AIService**: Interfaces with OpenAI API
  - **ResumeParser**: Extracts information from PDFs

### Data Flow

#### Interview Creation Flow
```
1. User uploads resume
   └─> ResumeParser extracts skills & experience
   └─> Resume saved to database

2. User selects job role and starts interview
   └─> Interview session created
   └─> AIService generates contextual questions
   └─> Questions saved to database

3. User answers questions
   └─> Response submitted to backend
   └─> AIService evaluates response
   └─> Evaluation scores saved
   └─> Feedback generated

4. Interview completed
   └─> Final scores calculated
   └─> Comprehensive report generated
   └─> Results displayed to user
```

## Database Schema

```sql
-- Job Roles
CREATE TABLE api_jobrole (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255) UNIQUE,
    description TEXT,
    required_skills JSON,
    experience_level VARCHAR(50),
    created_at DATETIME
);

-- Resumes
CREATE TABLE api_resume (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    file VARCHAR(100),
    full_text TEXT,
    skills JSON,
    experience_years INTEGER,
    contact_info JSON,
    uploaded_at DATETIME,
    updated_at DATETIME
);

-- Interviews
CREATE TABLE api_interview (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    job_role_id INTEGER,
    resume_id INTEGER,
    status VARCHAR(20),
    started_at DATETIME,
    completed_at DATETIME,
    duration_seconds INTEGER,
    overall_score FLOAT,
    feedback_report TEXT,
    created_at DATETIME,
    updated_at DATETIME
);

-- Interview Questions
CREATE TABLE api_interviewquestion (
    id INTEGER PRIMARY KEY,
    interview_id INTEGER,
    question_text TEXT,
    question_number INTEGER,
    created_at DATETIME
);

-- Interview Responses
CREATE TABLE api_interviewresponse (
    id INTEGER PRIMARY KEY,
    interview_id INTEGER,
    question_id INTEGER,
    response_text TEXT,
    response_audio VARCHAR(100),
    response_video VARCHAR(100),
    delivery_method VARCHAR(20),
    overall_score FLOAT,
    relevance_score FLOAT,
    completeness_score FLOAT,
    technical_depth_score FLOAT,
    communication_score FLOAT,
    experience_score FLOAT,
    strengths JSON,
    areas_for_improvement JSON,
    feedback TEXT,
    follow_up_question TEXT,
    evaluation_completed BOOLEAN,
    submitted_at DATETIME,
    evaluated_at DATETIME
);

-- Interview Feedback
CREATE TABLE api_interviewfeedback (
    id INTEGER PRIMARY KEY,
    interview_id INTEGER UNIQUE,
    overall_performance_summary TEXT,
    key_strengths JSON,
    areas_for_improvement JSON,
    technical_competency_assessment TEXT,
    behavioral_assessment TEXT,
    recommendations JSON,
    next_steps TEXT,
    generated_at DATETIME
);
```

## API Endpoints Summary

```
POST   /api/resumes/                           - Upload resume
GET    /api/resumes/{id}/                      - Get resume details

POST   /api/interviews/                        - Create interview
GET    /api/interviews/                        - List interviews
GET    /api/interviews/{id}/                   - Get interview details
POST   /api/interviews/{id}/start_interview/   - Start & generate questions
POST   /api/interviews/{id}/submit_response/   - Submit & evaluate response
GET    /api/interviews/{id}/get_next_question/ - Get next question
POST   /api/interviews/{id}/complete_interview/- Complete interview

GET    /api/job-roles/                         - List job roles
POST   /api/job-roles/                         - Create job role
GET    /api/job-roles/{id}/                    - Get job role details
```

## Key Technologies

### OpenAI Integration
- **Models Used**: GPT-3.5-turbo (default), GPT-4 (optional)
- **Temperature**: 0.7 (balanced creativity and consistency)
- **Max Tokens**: 2000-2500 per response

### Resume Processing
- PDF extraction using PyPDF2
- Regex-based skill matching
- Contact information extraction

### Evaluation Metrics
- Relevance: How well answer addresses question
- Completeness: Coverage of key points
- Technical Depth: Level of technical knowledge
- Communication: Clarity and structure
- Experience: Demonstration of relevant experience
- Overall: Weighted average of all metrics

## Scalability Considerations

### Current (SQLite)
- Single-file database
- Good for development
- Limited concurrent access

### Production (PostgreSQL)
- Multi-user support
- Better performance
- Advanced features (JSON support, indexing)

### Future Enhancements
- Caching layer (Redis)
- Message queue (Celery)
- File storage (S3)
- Rate limiting
- Load balancing

---

Last Updated: May 5, 2026
