#!/usr/bin/env python
"""
Simple startup script for Face Recognition Attendance System
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendancesite.settings')
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    print("🚀 Starting Face Recognition Attendance System...")
    print("📍 Server will run on: http://127.0.0.1:8000/")
    print("📊 Admin Panel: http://127.0.0.1:8000/admin/")
    print("📈 Dashboard: http://127.0.0.1:8000/dashboard/")
    print("👤 Admin Login: admin / admin123")
    print("\n" + "="*50)
    
    # Start the server
    execute_from_command_line(['manage.py', 'runserver', '127.0.0.1:8000'])