# Deployment Guide

## 🚀 Production Deployment

This guide covers deploying the AI Mock Interview System to production.

## 📋 Pre-Deployment Checklist

### Security
- [ ] Change SECRET_KEY in settings
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up HTTPS/SSL
- [ ] Implement authentication
- [ ] Add CSRF protection
- [ ] Review CORS settings
- [ ] Secure OpenAI API key

### Infrastructure
- [ ] Choose hosting platform
- [ ] Set up database (PostgreSQL)
- [ ] Configure file storage
- [ ] Set up CDN for static files
- [ ] Configure backup strategy
- [ ] Set up monitoring

### Performance
- [ ] Enable caching
- [ ] Optimize database queries
- [ ] Configure rate limiting
- [ ] Set up load balancing
- [ ] Optimize static files

## 🏠 Hosting Options

### Option 1: AWS (Recommended)

#### Backend (Elastic Beanstalk)
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 mock-interview-api

# Create environment
eb create production

# Deploy
eb deploy

# View logs
eb logs
```

#### Database (RDS PostgreSQL)
1. Create RDS instance
2. Update settings.py with database URL
3. Run migrations on RDS

#### File Storage (S3)
```python
# settings.py
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_STORAGE_BUCKET_NAME = 'your-bucket'
AWS_ACCESS_KEY_ID = 'your-key'
AWS_SECRET_ACCESS_KEY = 'your-secret'
```

### Option 2: Heroku

#### Backend Deployment
```bash
# Install Heroku CLI
# Login
heroku login

# Create app
heroku create mock-interview-api

# Set environment variables
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set SECRET_KEY=your-secret
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# View logs
heroku logs --tail
```

#### Frontend Deployment
```bash
# Similar process for Streamlit
# Or use Streamlit Cloud (recommended)
```

### Option 3: Docker Containerization

#### Create Dockerfile for Backend
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "interview_system.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### Create docker-compose.yml
```yaml
version: '3'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: interview_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  web:
    build: ./backend
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=True
      - OPENAI_API_KEY=sk-...
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "8501:8501"
    command: streamlit run app.py --server.port=8501
    environment:
      - API_BASE_URL=http://web:8000/api
    depends_on:
      - web

volumes:
  postgres_data:
```

Deploy with Docker:
```bash
docker-compose up -d
```

## 🗄️ Database Migration

### From SQLite to PostgreSQL

1. **Backup SQLite database**
```bash
python manage.py dumpdata > data.json
```

2. **Update settings.py**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'interview_db',
        'USER': 'postgres',
        'PASSWORD': 'your-password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

3. **Install PostgreSQL adapter**
```bash
pip install psycopg2-binary
```

4. **Create database**
```bash
createdb interview_db
```

5. **Run migrations**
```bash
python manage.py migrate
python manage.py loaddata data.json
```

## 🔐 Security Configuration

### Production settings.py
```python
# Security
DEBUG = False
SECRET_KEY = 'your-random-secret-key'
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# HTTPS
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# CORS
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = '/app/staticfiles'

# Media files (use S3 for production)
MEDIA_URL = 'https://s3.amazonaws.com/bucket/'
MEDIA_ROOT = '/tmp/media'
```

### Environment Variables
```env
SECRET_KEY=your-random-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
OPENAI_API_KEY=sk-your-api-key
DATABASE_URL=postgresql://user:password@host:5432/dbname
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=your-bucket
```

## 📊 Monitoring & Logging

### Set up Monitoring
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django.log',
        },
    },
    'root': {
        'handlers': ['file'],
        'level': 'ERROR',
    },
}
```

### Use Services
- **Sentry** for error tracking
- **DataDog** for monitoring
- **New Relic** for performance
- **CloudWatch** for AWS logs

## 🔄 CI/CD Pipeline

### GitHub Actions Example
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    
    - name: Install dependencies
      run: |
        cd backend
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        cd backend
        python manage.py test
    
    - name: Deploy to production
      run: |
        # Add your deployment commands here
        eb deploy
```

## 🚀 Deployment Steps Summary

### For AWS Elastic Beanstalk:
1. Configure EB environment
2. Set environment variables
3. Run migrations: `eb open && python manage.py migrate`
4. Deploy: `eb deploy`

### For Heroku:
1. Create Procfile
2. Set config vars
3. Deploy: `git push heroku main`
4. Run migrations: `heroku run python manage.py migrate`

### For Docker:
1. Build images: `docker-compose build`
2. Run containers: `docker-compose up -d`
3. Run migrations: `docker-compose exec web python manage.py migrate`

## 📈 Post-Deployment

### Health Checks
```bash
# Check backend
curl https://yourdomain.com/api/job-roles/

# Check frontend
curl https://yourdomain.com/
```

### Backup Strategy
- Daily database backups
- Weekly full backups
- Monthly archive to cold storage
- Test restore procedures regularly

### Performance Optimization
- Enable gzip compression
- Minify static files
- Use CDN for static assets
- Configure caching headers
- Set up database indexes

### Scaling
- Use auto-scaling groups
- Load balance across servers
- Cache frequently accessed data
- Optimize database queries
- Monitor resource usage

## 🆘 Troubleshooting

### Application Won't Start
```bash
# Check logs
heroku logs --tail
eb logs

# Check environment variables
heroku config
eb printenv
```

### Database Connection Errors
```bash
# Check connection string
echo $DATABASE_URL

# Test connection
psql $DATABASE_URL
```

### High Memory Usage
```bash
# Profile memory
python manage.py shell
import tracemalloc
tracemalloc.start()
```

### Slow Performance
```bash
# Check slow queries
python manage.py shell_plus
from django.db import connection
print(connection.queries)
```

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Heroku Python Support](https://devcenter.heroku.com/articles/getting-started-with-python)
- [AWS Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/)
- [Docker Documentation](https://docs.docker.com/)
- [Streamlit Deployment](https://docs.streamlit.io/streamlit-cloud/deploy-your-app)

---

**Last Updated**: May 5, 2026
