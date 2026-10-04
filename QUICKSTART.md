# Quick Start Guide

## 🚀 Getting Started in 5 Minutes

### Prerequisites
- Python 3.8 or higher
- OpenAI API Key (get one from https://platform.openai.com/api-keys)
- Git

### Step 1: Clone and Navigate
```bash
cd "ai power mock interview system"
```

### Step 2: Setup Backend

**Windows:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 3: Configure Backend

Create `.env` file in `backend/` directory:
```env
SECRET_KEY=django-insecure-dev-key-change-in-production
DEBUG=True
OPENAI_API_KEY=your-openai-api-key-here
```

### Step 4: Initialize Database

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py load_sample_jobs
```

### Step 5: Start Backend Server

```bash
python manage.py runserver
```

✅ Backend running at: http://localhost:8000

### Step 6: Setup Frontend

Open a new terminal, then:

**Windows:**
```bash
cd frontend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
cd frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 7: Configure Frontend

Create `.env` file in `frontend/` directory:
```env
API_BASE_URL=http://localhost:8000/api
DEBUG=False
```

### Step 8: Start Frontend

```bash
streamlit run app.py
```

✅ Frontend running at: http://localhost:8501

---

## 📝 Using the System

### Home Page
1. Review the introduction and features
2. Understand the workflow

### Upload Resume
1. Click "Upload Resume" in sidebar
2. Upload your PDF resume
3. Review extracted skills and experience

### Browse Jobs
1. Explore available job roles
2. Filter by experience level
3. View job descriptions and requirements

### Start Interview
1. Select a job role
2. Choose number of questions (3-10)
3. Click "Start Interview"

### Conduct Interview
1. Read each question carefully
2. Type or speak your answer
3. Submit for AI evaluation
4. Review immediate feedback
5. Move to next question

### View Feedback
1. See overall score and metrics
2. Read detailed feedback for each response
3. Check strengths and areas for improvement
4. Review comprehensive report

### Review History
1. See all past interviews
2. Track your progress
3. Compare scores over time

---

## 🔧 Troubleshooting

### Backend won't start
```bash
# Clear cache
python manage.py clear_cache

# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Frontend can't connect to backend
- Verify backend is running on http://localhost:8000
- Check API_BASE_URL in frontend/.env
- Verify CORS settings in backend

### OpenAI API errors
- Check your API key is correct
- Verify you have credits in OpenAI account
- Check rate limits

### Resume upload fails
- Ensure file is a valid PDF
- Check file size (should be < 10MB)
- Try converting to PDF if using Word

---

## 📚 Admin Interface

Access Django admin at: http://localhost:8000/admin

Login with superuser credentials created earlier.

### Admin Features:
- Add/edit job roles
- Manage resumes
- View and analyze interviews
- Check evaluation results

---

## 📊 Architecture Overview

```
User (Streamlit Frontend)
        ↓
     (HTTP/REST)
        ↓
Django Backend API
    ├── Resume Parser
    ├── Interview Engine
    └── OpenAI AI Service
        ↓
    SQLite Database
```

---

## 🎯 Next Steps

1. **Explore Sample Resumes**: Create test resumes to see how the system works
2. **Try Different Roles**: Practice for multiple job positions
3. **Analyze Feedback**: Review patterns in your responses
4. **Iterate & Improve**: Use feedback to enhance your interview skills
5. **Track Progress**: Monitor improvements across multiple sessions

---

## 📖 Full Documentation

See [README.md](README.md) for comprehensive documentation including:
- API documentation
- Configuration options
- Deployment guide
- Troubleshooting tips
- Advanced features

---

## 💡 Tips for Best Results

1. **Use Real Resume**: Upload your actual resume for personalized questions
2. **Answer Thoroughly**: Provide detailed responses for better evaluation
3. **Practice Regularly**: Multiple sessions improve performance
4. **Review Feedback**: Focus on areas marked for improvement
5. **Time Yourself**: Keep track of how long answers take

---

**Happy Interviewing! 🎉**
