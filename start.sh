#!/bin/bash
# Windows startup script for development

echo "=========================================="
echo "AI Mock Interview System - Development"
echo "=========================================="
echo ""

# Check if in correct directory
if [ ! -f "setup.bat" ]; then
    echo "Error: Please run this script from the project root directory"
    exit 1
fi

# Create .env files if they don't exist
if [ ! -f "backend/.env" ]; then
    echo "Creating backend/.env from template..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please edit backend/.env and add your OpenAI API key"
fi

if [ ! -f "frontend/.env" ]; then
    echo "Creating frontend/.env from template..."
    cp frontend/.env.example frontend/.env
fi

echo ""
echo "Starting backend and frontend..."
echo ""

# Start backend in background
echo "Starting Django backend server..."
cd backend
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate
python manage.py migrate
python manage.py runserver &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "Starting Streamlit frontend..."
cd frontend
source venv/bin/activate 2>/dev/null || . venv/Scripts/activate
streamlit run app.py &
FRONTEND_PID=$!
cd ..

echo ""
echo "=========================================="
echo "✅ System is running!"
echo "=========================================="
echo ""
echo "Backend:  http://localhost:8000"
echo "Admin:    http://localhost:8000/admin"
echo "API:      http://localhost:8000/api"
echo "Frontend: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Wait for both processes
wait

echo ""
echo "Shutting down..."
kill $BACKEND_PID $FRONTEND_PID
exit 0
