# 🚀 Quick Start Guide - Face Recognition Attendance System

<div align="center">

![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)
![Status](https://img.shields.io/badge/status-Ready%20to%20Use-brightgreen.svg)

</div>

## ✅ System Status: READY TO USE

Your Face Recognition Attendance System is fully configured and operational!

## 📋 Table of Contents

- [Access Information](#-access-information)
- [Quick Actions](#-quick-actions)
- [Project Structure](#-project-structure)
- [Key Features](#-key-features)
- [Customization](#-customization)
- [Troubleshooting](#-troubleshooting)

## 🌐 Access Information

### Application URLs

| Component | URL | Description |
|-----------|-----|-------------|
| Main Application | http://127.0.0.1:8000/ | Mark attendance with facial recognition |
| Admin Dashboard | http://127.0.0.1:8000/admin/ | Django admin interface |
| Attendance Dashboard | http://127.0.0.1:8000/dashboard/ | View and manage attendance data |
| Registration | http://127.0.0.1:8000/register/ | Register new students |

### Default Admin Credentials

- **Username**: admin
- **Password**: admin123

## 🎯 Quick Actions

### Mark Attendance

1. Navigate to http://127.0.0.1:8000/
2. Allow camera permissions when prompted
3. Position your face in the camera frame
4. Click "Capture & Mark Attendance"
5. Receive confirmation of successful attendance

### View Attendance Data

1. Go to http://127.0.0.1:8000/dashboard/
2. View attendance statistics and records
3. Use filters to search by date, student, or month
4. Export data to Excel using the export buttons

### Register New Students

1. Navigate to http://127.0.0.1:8000/register/
2. Fill in the student details (name, ID, email)
3. Upload a clear front-facing photo
4. Submit the form

### Use AI Assistant

On the dashboard, use the AI chatbot to ask questions like:
- "How many students attended today?"
- "Show me attendance for [student name]"
- "What's the attendance percentage this month?"
- "How do I export attendance data?"

## 📁 Project Structure

```
attendancesite/
├── attendancesite/          # Django project settings
├── faceapp/                 # Main application
│   ├── templates/           # HTML templates
│   │   ├── base.html        # Base template with navigation
│   │   ├── dashboard.html   # Dashboard interface
│   │   ├── index.html       # Home page with webcam
│   │   └── register.html    # Student registration form
│   ├── static/              # Static assets (CSS, JS, images)
│   ├── models.py            # Database models
│   ├── views.py             # Application logic
│   └── urls.py              # URL routing
├── known_faces/             # Student photos for recognition
├── media/                   # Uploaded files
│   └── student_photos/      # Uploaded student photos
├── requirements.txt         # Python dependencies
├── README.md                # Full documentation
└── manage.py                # Django management script
```

## 🔧 Key Features

### Core Features

- ✅ **Face Recognition**: Accurate face detection using OpenCV
- ✅ **Real-time Attendance**: Instant attendance marking
- ✅ **Comprehensive Dashboard**: Statistics and data visualization
- ✅ **Student Management**: Registration and profile management
- ✅ **Export Functionality**: Excel export in multiple formats

### Advanced Features

- ✅ **AI Chatbot**: Natural language queries for attendance data
- ✅ **Multi-filter System**: Filter by date, student, or month
- ✅ **Responsive Design**: Works on desktop and mobile devices
- ✅ **Google Sheets Integration**: Ready to configure
- ✅ **Security Features**: CSRF protection, input validation

## 🎨 Customization

### Adding Student Photos

The recommended way to add students is through the registration page:
1. Navigate to http://127.0.0.1:8000/register/
2. Complete the registration form with student details
3. Upload a clear photo for facial recognition

Alternatively, you can manually add photos:
1. Place student photos in the `known_faces/` directory
2. Name files using the student ID (e.g., `123456.jpg`)

### Google Sheets Integration

1. Create a project in Google Cloud Console
2. Enable Google Sheets API
3. Create service account credentials
4. Download `credentials.json` and place it in the project root
5. Create a Google Sheet named "Attendance Sheet"
6. Share the sheet with your service account email

## 🔍 Troubleshooting

### Camera Issues

- Ensure your browser has permission to access the camera
- Try using Chrome or Firefox for best compatibility
- Check that no other application is using the camera

### Face Recognition Problems

- Ensure good lighting conditions
- Use a clear, front-facing photo for registration
- Position your face properly in the camera frame

### Server Issues

- Check that the Django server is running
- Verify port 8000 is not in use by another application
- Restart the server if needed: `python manage.py runserver`

---

<div align="center">

For complete documentation, refer to the [README.md](README.md) file.

**Built with ❤️ for Dr. C.V. Raman University Khandwa**

</div>