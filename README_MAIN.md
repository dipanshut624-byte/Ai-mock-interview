# AI-Powered Mock Interview System

A comprehensive platform for students and professionals to practice interviews with AI-powered feedback, developed using Django + Streamlit + OpenAI.

## 🎯 Project Overview

This system addresses the problem that **students lack exposure to real interview environments and structured feedback** by providing:

- **AI-Generated Questions**: Personalized based on your resume and target job role
- **Real-Time Evaluation**: Instant scoring and feedback on your responses
- **Comprehensive Feedback**: Detailed reports with strengths and areas for improvement
- **Progress Tracking**: Monitor your performance across multiple interview sessions

## ✨ Key Features

### 🎤 Interview System
- Resume upload and intelligent parsing
- AI-powered question generation
- Real-time response evaluation
- Detailed performance metrics
- Interview history and analytics

### 🤖 AI Integration
- OpenAI GPT-based question generation
- Contextual evaluation using multiple metrics
- Follow-up question suggestions
- Comprehensive feedback generation

### 📊 Evaluation Metrics
- Overall Score (0-100)
- Relevance, Completeness, Technical Depth
- Communication and Experience Scores
- Strengths and improvement suggestions

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API Key

### Setup (5 minutes)

**Backend:**
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # or: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add your OpenAI API key to .env
python manage.py migrate
python manage.py load_sample_jobs
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
python -m venv venv
venv\Scripts\activate  # or: source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

Access at:
- Frontend: http://localhost:8501
- Backend: http://localhost:8000
- Admin: http://localhost:8000/admin

See [QUICKSTART.md](QUICKSTART.md) for detailed setup instructions.

## 📁 Project Structure

```
ai-mock-interview-system/
├── backend/              # Django REST API
│   ├── interview_system/
│   │   ├── core/         # AI & Resume services
│   │   └── api/          # Models, views, serializers
│   └── manage.py
├── frontend/             # Streamlit UI
│   ├── app.py            # Main application
│   ├── pages/            # Interview pages
│   └── utils.py          # API client
├── README.md             # This file
├── QUICKSTART.md         # 5-minute setup guide
├── ARCHITECTURE.md       # Technical architecture
├── DEVELOPMENT.md        # Development guide
├── DEPLOYMENT.md         # Production deployment
└── FEATURES.md           # Features & roadmap
```

## 🛠️ Tech Stack

- **Backend**: Django 4.2, Django REST Framework
- **Frontend**: Streamlit
- **AI**: OpenAI GPT-3.5/4
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Processing**: PyPDF2 (resume parsing), SpeechRecognition (audio)

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development setup & tips
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment
- **[FEATURES.md](FEATURES.md)** - Features & roadmap
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contributing guide

## 🔄 Workflow

1. **Upload Resume** → System extracts skills and experience
2. **Select Job Role** → Choose target position
3. **Start Interview** → AI generates personalized questions
4. **Answer Questions** → Provide text responses
5. **Receive Feedback** → Get instant evaluation and suggestions
6. **Track Progress** → Monitor improvements over time

## 🧪 Testing

```bash
cd backend
python manage.py test
```

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for:
- AWS Elastic Beanstalk
- Heroku
- Docker
- Security configuration
- Database migration

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Steps
1. Fork repository
2. Create feature branch: `git checkout -b feature/your-feature`
3. Make changes and test
4. Commit: `git commit -m "feat: description"`
5. Push and create Pull Request

## 📋 Roadmap

### Current (v1.0.0)
- ✅ Text-based interviews
- ✅ Resume parsing
- ✅ AI evaluation
- ✅ History tracking

### Planned
- 🎙️ Audio responses (v1.1.0)
- 📹 Video recording (v1.2.0)
- 👤 User authentication (v1.2.0)
- 📱 Mobile app (v2.0.0)
- 📊 Analytics dashboard (v1.1.0)

See [FEATURES.md](FEATURES.md) for complete roadmap.

## ⚙️ Configuration

### Environment Variables

**Backend (.env):**
```env
SECRET_KEY=your-secret-key
DEBUG=False
OPENAI_API_KEY=sk-your-api-key
DATABASE_URL=sqlite:///db.sqlite3
```

**Frontend (.env):**
```env
API_BASE_URL=http://localhost:8000/api
DEBUG=False
```

## 🆘 Troubleshooting

### Backend won't start
```bash
python manage.py migrate
python manage.py runserver
```

### Frontend can't connect
- Check backend is running on http://localhost:8000
- Verify API_BASE_URL in frontend/.env

### OpenAI errors
- Verify API key is correct
- Check account credits
- Ensure proper permissions

See [DEVELOPMENT.md](DEVELOPMENT.md) for more troubleshooting tips.

## 📈 Performance

Current metrics:
- Question generation: ~2-3 seconds
- Response evaluation: ~3-5 seconds
- Resume parsing: ~1-2 seconds
- Page load time: <1 second

## 🔐 Security

- HTTPS ready
- CORS configured
- SQL injection protection
- CSRF protection
- Secure API endpoints

See [DEPLOYMENT.md](DEPLOYMENT.md) for production security setup.

## 📊 API Documentation

Base URL: `http://localhost:8000/api`

### Key Endpoints
```
POST   /interviews/                        Create interview
POST   /interviews/{id}/start_interview/   Generate questions
POST   /interviews/{id}/submit_response/   Evaluate response
GET    /interviews/{id}/                   Get details
POST   /resumes/                           Upload resume
GET    /job-roles/                         List job roles
```

See [ARCHITECTURE.md](ARCHITECTURE.md) for complete API docs.

## 💾 Database

### Models
- JobRole
- Resume
- Interview
- InterviewQuestion
- InterviewResponse
- InterviewFeedback

### ERD
See [ARCHITECTURE.md](ARCHITECTURE.md) for database schema.

## 🎓 Use Cases

1. **Students** - Prepare for job interviews
2. **Career Changers** - Practice new field interviews
3. **Remote Candidates** - Practice before real interviews
4. **Companies** - Conduct pre-screening interviews
5. **Coaches** - Help clients with interview prep

## 📞 Support

- 📧 Email: support@mockinterview.ai
- 💬 GitHub Issues: Bug reports & features
- 📚 Documentation: [This repo](/)
- 🤝 Community: Discussions (coming soon)

## 🙏 Acknowledgments

Built with:
- [Django](https://www.djangoproject.com/)
- [Streamlit](https://streamlit.io/)
- [OpenAI](https://openai.com/)
- [Python](https://www.python.org/)

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

## 🎯 Vision

Make quality interview preparation **accessible to everyone** through AI-powered feedback and personalized learning.

---

**Version**: 1.0.0 | **Last Updated**: May 5, 2026 | **Status**: ✅ Production Ready
