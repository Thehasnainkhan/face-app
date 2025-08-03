@echo off
echo Starting Face Recognition Attendance System...
echo.
echo Server will run on: http://127.0.0.1:8000/
echo Admin Panel: http://127.0.0.1:8000/admin/
echo Dashboard: http://127.0.0.1:8000/dashboard/
echo Admin Login: admin / admin123
echo.
cd /d "%~dp0"
call venv\Scripts\activate
python manage.py runserver 127.0.0.1:8000
pause