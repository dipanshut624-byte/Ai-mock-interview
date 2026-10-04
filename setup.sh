#!/bin/bash
# Setup script for AI Mock Interview System

echo "🚀 Setting up AI Mock Interview System..."

# Create backend virtual environment
echo "Setting up backend..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
python manage.py migrate
python manage.py createsuperuser

# Create frontend virtual environment
echo "Setting up frontend..."
cd ../frontend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "To start the system:"
echo "1. Backend: cd backend && source venv/bin/activate && python manage.py runserver"
echo "2. Frontend: cd frontend && source venv/bin/activate && streamlit run app.py"
