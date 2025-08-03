#!/usr/bin/env python
"""
Setup script for Face Recognition Attendance System
"""
import os
import sys
import django
from pathlib import Path

def setup_project():
    """Setup the Django project"""
    print("🚀 Setting up Face Recognition Attendance System...")
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendancesite.settings')
    django.setup()
    
    from django.core.management import execute_from_command_line
    
    # Run migrations
    print("📊 Running database migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Create superuser if it doesn't exist
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        print("👤 Creating admin user...")
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        print("✅ Admin user created:")
        print("   Username: admin")
        print("   Password: admin123")
    
    # Create known_faces directory if it doesn't exist
    known_faces_dir = Path('known_faces')
    if not known_faces_dir.exists():
        known_faces_dir.mkdir()
        print("📁 Created known_faces directory")
    
    # Create media directory for student photos
    media_dir = Path('media')
    if not media_dir.exists():
        media_dir.mkdir()
        print("📁 Created media directory")
    
    print("\n✅ Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Run the server: python manage.py runserver")
    print("2. Access the application: http://127.0.0.1:8000/")
    print("3. Admin panel: http://127.0.0.1:8000/admin/")
    print("4. Dashboard: http://127.0.0.1:8000/dashboard/")
    print("\n🔧 Optional setup:")
    print("- Add student photos to known_faces/ directory")
    print("- Configure Google Sheets integration (see README.md)")
    print("- Customize the application as needed")

if __name__ == '__main__':
    setup_project()