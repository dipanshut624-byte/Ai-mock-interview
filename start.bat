@echo off
REM Windows startup script for development

echo ==========================================
echo AI Mock Interview System - Development
echo ==========================================
echo.

REM Check if in correct directory
if not exist "setup.bat" (
    echo Error: Please run this script from the project root directory
    exit /b 1
)

REM Create .env files if they don't exist
if not exist "backend\.env" (
    echo Creating backend\.env from template...
    copy backend\.env.example backend\.env
    echo Warning: Please edit backend\.env and add your OpenAI API key
)

if not exist "frontend\.env" (
    echo Creating frontend\.env from template...
    copy frontend\.env.example frontend\.env
)

echo.
echo Starting backend and frontend...
echo.

REM Start backend
echo Starting Django backend server...
cd backend
call venv\Scripts\activate
python manage.py migrate
start python manage.py runserver
cd ..

REM Wait a moment for backend to start
timeout /t 3 /nobreak

REM Start frontend
echo Starting Streamlit frontend...
cd frontend
call venv\Scripts\activate
streamlit run app.py
cd ..
