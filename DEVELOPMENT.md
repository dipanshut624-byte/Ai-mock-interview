# Development Setup

## 📋 Prerequisites

Before you begin, make sure you have:
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment tool (venv - comes with Python)
- OpenAI API key (https://platform.openai.com/api-keys)
- Text editor or IDE (VS Code, PyCharm, etc.)

## 🔑 Getting Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign up or log in to your OpenAI account
3. Create a new API key
4. Keep it secure - never share it publicly
5. You'll get a key like `sk-...`

## 💻 Backend Setup (Django)

### 1. Navigate to Backend Directory
```bash
cd backend
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Environment Configuration
```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# On Windows, you can use:
# copy .env.example .env
```

Edit `.env` file:
```env
SECRET_KEY=django-insecure-your-secret-key
DEBUG=True
OPENAI_API_KEY=sk-your-api-key-here
```

### 5. Initialize Database
```bash
python manage.py migrate
```

### 6. Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### 7. Load Sample Job Roles
```bash
python manage.py load_sample_jobs
```

### 8. Run Development Server
```bash
python manage.py runserver
```

Visit http://localhost:8000 to verify backend is running.
Admin panel: http://localhost:8000/admin

## 🎨 Frontend Setup (Streamlit)

### 1. Open New Terminal and Navigate to Frontend
```bash
cd frontend
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Environment Configuration
```bash
# Copy the example file
cp .env.example .env

# Edit .env to configure API URL
```

Edit `.env` file:
```env
API_BASE_URL=http://localhost:8000/api
DEBUG=False
```

### 5. Run Streamlit App
```bash
streamlit run app.py
```

Visit http://localhost:8501 in your browser.

## ✅ Verification Checklist

- [ ] Backend running at http://localhost:8000
- [ ] Backend API accessible at http://localhost:8000/api
- [ ] Admin panel accessible at http://localhost:8000/admin
- [ ] Frontend running at http://localhost:8501
- [ ] Can access home page in Streamlit
- [ ] Job roles loaded (visible in "Browse Jobs")

## 🧪 Testing the System

### Test Flow:
1. **Upload Resume**: Navigate to "Upload Resume" page
2. **Select Job Role**: Go to "Browse Jobs" and select a role
3. **Start Interview**: Click "Start Interview" button
4. **Answer Questions**: Respond to generated questions
5. **Review Feedback**: Check your scores and feedback

## 🔧 Troubleshooting

### Backend Won't Start
```bash
# Clear Python cache
python manage.py clear_cache

# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
python manage.py load_sample_jobs
```

### Frontend Can't Connect
- Check backend is running: `http://localhost:8000`
- Verify API_BASE_URL in frontend/.env
- Check for CORS errors in browser console
- Ensure Django DEBUG=True during development

### OpenAI API Errors
- Verify API key is correct: `sk-...`
- Check you have credits in OpenAI account
- Verify API key has access to `gpt-3.5-turbo` model
- Check rate limits in OpenAI dashboard

### Resume Upload Issues
- Ensure file is a valid PDF (not corrupted)
- Check file size (should be < 10MB)
- Verify resume has readable text
- Try copying text to .txt file and uploading

## 📚 Admin Panel Features

### Access Admin Panel
1. Go to http://localhost:8000/admin
2. Log in with superuser credentials
3. Manage:
   - Job Roles
   - Resumes
   - Interviews
   - Interview Questions
   - Interview Responses

### Add New Job Role
1. Click "Job roles" in admin
2. Click "Add Job role"
3. Fill in:
   - Name (e.g., "Full Stack Engineer")
   - Description
   - Required skills (JSON array)
   - Experience level

Example:
```json
["Python", "Django", "React", "PostgreSQL"]
```

## 📝 Database Management

### View Database
```bash
# Using Django shell
python manage.py shell

# List all resumes
from api.models import Resume
Resume.objects.all()

# List all interviews
from api.models import Interview
Interview.objects.all()
```

### Reset Database
```bash
# Delete database file
rm db.sqlite3

# Recreate
python manage.py migrate
python manage.py createsuperuser
python manage.py load_sample_jobs
```

## 🚀 Next Steps

1. **Experiment**: Try different resumes and job roles
2. **Analyze Feedback**: Review evaluation metrics
3. **Iterate**: Answer same questions multiple times to improve
4. **Explore Code**: Understand the architecture
5. **Customize**: Modify prompts and evaluation criteria

## 📖 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [OpenAI API Documentation](https://platform.openai.com/docs/api-reference)
- [Django REST Framework](https://www.django-rest-framework.org/)

## 💡 Development Tips

### Keep Terminals Organized
- Terminal 1: Backend (`python manage.py runserver`)
- Terminal 2: Frontend (`streamlit run app.py`)
- Terminal 3: Other commands (git, testing, etc.)

### Use VS Code Extensions
- Python (Microsoft)
- Django (Baptiste Darthenay)
- Streamlit (Alzenor Chavez)

### Debug Mode
- Django: Set `DEBUG=True` in .env
- Streamlit: Uses hot-reload by default
- OpenAI: Check API responses in Django logs

## 🤝 Contributing

To contribute to development:
1. Create a new branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Test thoroughly
4. Commit with clear messages
5. Push and create pull request

## 📞 Getting Help

If you encounter issues:
1. Check [QUICKSTART.md](../QUICKSTART.md)
2. Review [ARCHITECTURE.md](../ARCHITECTURE.md)
3. Check Django logs
4. Search existing issues
5. Create a new issue with details

---

**Last Updated**: May 5, 2026
