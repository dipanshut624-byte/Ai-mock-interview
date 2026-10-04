@echo off
REM Setup script for AI Mock Interview System on Windows

echo Setting up AI Mock Interview System...

REM Create backend virtual environment
echo Setting up backend...
cd backend
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt

REM Initialize database
echo Initializing database...
python manage.py migrate
python manage.py createsuperuser

REM Create frontend virtual environment
echo Setting up frontend...
cd ..\frontend
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo To start the system:
echo 1. Backend: cd backend && venv\Scripts\activate.bat && python manage.py runserver
echo 2. Frontend: cd frontend && venv\Scripts\activate.bat && streamlit run app.py
pause
