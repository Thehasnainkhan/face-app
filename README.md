# Face Recognition Attendance System

<div align="center">

![Version](https://img.shields.io/badge/version-1.3.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.8+-green.svg)
![Django](https://img.shields.io/badge/Django-5.2.4-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

</div>

A modern, web-based attendance management system powered by facial recognition technology. Built with Django, OpenCV, and modern web technologies for educational institutions.

## 📑 Table of Contents

- [Features](#-features)
- [Technology Stack](#️-technology-stack)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage Guide](#-usage-guide)
- [API Reference](#-api-reference)
- [Customization](#-customization)
- [Security](#-security)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Support](#-support)

## 🖥️ How to Run This Project in VS Code (Beginner Friendly)

**Follow these simple steps to get the project running:**

1. **Open the Project Folder**
   - Open VS Code.
   - Go to `File > Open Folder...` and select the `attendancesite` folder.

2. **Install Python & the Python Extension**
   - Make sure Python 3.8+ is installed on your computer.
   - In VS Code, go to the Extensions tab (left sidebar) and install the "Python" extension by Microsoft.

3. **Open the Terminal in VS Code**
   - Go to `View > Terminal` or press <kbd>Ctrl</kbd> + <kbd>`</kbd> (backtick).

4. **Activate the Virtual Environment**
   - If your terminal prompt starts with `(venv)`, skip this step (already activated).
   - Otherwise, type one of these and press Enter:
     ```powershell
     .\venv\Scripts\activate
     ```
     or
     ```powershell
     .\.venv\Scripts\activate
     ```

5. **Install the Requirements**
   ```powershell
   pip install -r requirements.txt
   ```

6. **Run the Django Server**
   ```powershell
   python manage.py runserver
   ```

7. **Open Your Browser**
   - Go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to use the application.
   - For admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

**If you see any errors, copy them and ask for help!**

---

### Core Functionality

- **Facial Recognition**: Accurate face detection and recognition using OpenCV
- **Real-time Attendance**: Mark attendance instantly through webcam integration
- **Comprehensive Dashboard**: Analytics, filters, and data visualization
- **Student Management**: Register, view, and manage student profiles
- **Attendance Records**: Track, filter, and export attendance data

### Advanced Features

- **Google Sheets Integration**: Automatic syncing with Google Sheets
- **Excel Export**: Export attendance data in multiple formats
- **AI Chatbot Assistant**: Natural language queries for attendance data
- **Multi-filter System**: Filter by date, student name, or month
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🛠️ Technology Stack

### Backend
- **Framework**: Django 5.2.4
- **Database**: SQLite (configurable for PostgreSQL/MySQL)
- **Face Recognition**: OpenCV, face_recognition
- **Data Processing**: Pandas, NumPy

### Frontend
- **UI Framework**: Bootstrap 5
- **JavaScript**: ES6, jQuery
- **CSS**: Custom responsive design
- **Icons**: Font Awesome 6

### Integrations
- **Cloud Storage**: Google Sheets API
- **Export Engine**: OpenPyXL

## 💻 System Requirements

- **Python**: 3.8 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 500MB free space
- **Camera**: Webcam for face recognition
- **Browser**: Chrome, Firefox, Edge (latest versions)
- **Internet**: Required for Google Sheets integration

## 📦 Installation

### Quick Start

```bash
# Clone the repository (if using Git)
# git clone <repository-url>

# Navigate to project directory
cd attendancesite

# Run the setup script
python setup.py

# Or use the batch file on Windows
start.bat
```

### Running in VS Code

1. **Open the Project**
   - Launch VS Code and open the root project folder.

2. **Set Up the Virtual Environment**
   - Open a terminal in VS Code (`Terminal > New Terminal`).
   - Run:
     ```bash
     python -m venv venv
     venv\Scripts\activate  # On Windows
     # or
     source venv/bin/activate  # On macOS/Linux
     pip install -r requirements.txt
     ```

3. **Configure Environment Variables**
   - In VS Code, create a `.env` file or set environment variables in your launch configuration.
   - Set your OpenAI API key:
     ```env
     OPENAI_API_KEY=sk-...your-key...
     ```

4. **Run the Server**
   - Use the batch script (`start.bat`) or run directly:
     ```bash
     python manage.py runserver 127.0.0.1:8000
     ```
   - Access the app at [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

5. **Debugging**
   - Set breakpoints in VS Code.
   - Use the Python: Django debug configuration to start the server in debug mode.

### Project Structure

```
attendancesite/
├── attendancesite/         # Django project settings, URLs
├── faceapp/               # Main app: models, views, face recognition, chatbot
│   ├── models.py          # Student, Attendance, ChatHistory
│   ├── views.py           # All main views, AI assistant, chat export
│   ├── face_utils.py      # Face recognition logic
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS, images
├── known_faces/           # Saved face images for recognition
├── media/                 # Uploaded student photos
├── requirements.txt       # Python dependencies
├── start.bat              # Windows quick start script
├── README.md              # This file
├── db.sqlite3             # SQLite database
```

- **attendancesite/**: Django project config
- **faceapp/**: Main logic (students, attendance, AI assistant, chat export)
- **known_faces/**: Images used by face recognition
- **media/**: Uploaded files
- **requirements.txt**: All dependencies
- **start.bat**: Windows launch script

### New Features
- **AI Chatbot Assistant**: Ask any natural language attendance question; answers powered by OpenAI GPT-4o and your real data.
- **Chat Logging**: Every question/answer is saved (admin-only view/export).
- **Chat Export**: Download all chat history as CSV from `/export_chat_history/` endpoint.
- **API Key Security**: OpenAI API key is read from environment/config, not hardcoded.
- **Full Data Summarization**: Assistant uses all attendance data for smart answers.

### Usage Guide
- Register students, mark attendance via webcam, view analytics, ask the assistant anything about attendance.
- Export attendance or chat logs as Excel/CSV.
- Configure Google Sheets integration for cloud sync.

For detailed API and customization info, see the full documentation sections below.
```

### Manual Installation

1. **Set up virtual environment**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

2. **Configure the application**

```bash
# Navigate to project directory
cd attendancesite

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

3. **Access the application**

- Main Application: http://127.0.0.1:8000/
- Admin Dashboard: http://127.0.0.1:8000/admin/
- Attendance Dashboard: http://127.0.0.1:8000/dashboard/

## ⚙️ Configuration

### Database Configuration

Edit `attendancesite/settings.py` to change database:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Google Sheets Integration

1. Create a project in [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Google Sheets API
3. Create service account credentials
4. Download `credentials.json` and place it in the project root
5. Create a Google Sheet named "Attendance Sheet"
6. Share the sheet with your service account email

## 📱 Usage Guide

### For Students

1. Navigate to the home page
2. Allow camera permissions when prompted
3. Position your face in the camera frame
4. Click "Capture & Mark Attendance"
5. Receive confirmation of successful attendance

### For Administrators

1. Access the dashboard at `/dashboard/`
2. View attendance statistics and records
3. Register new students via the "Register" page
4. Use filters to search specific data
5. Export data to Excel format
6. Use the AI chatbot for quick attendance queries

## 📊 API Reference

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with webcam interface |
| `/upload_image/` | POST | Process face recognition and mark attendance |
| `/dashboard/` | GET | Admin dashboard with attendance data |
| `/register/` | GET/POST | Register new students |
| `/export/` | GET | Export attendance data to Excel |
| `/chatbot/` | POST | AI chatbot for attendance queries |
| `/delete_student/<id>/` | GET | Delete a student record |
| `/delete_attendance/<id>/` | GET | Delete an attendance record |

## 🎨 Customization

### Adding Student Photos

1. Register students through the registration page
2. Upload clear, front-facing photos
3. Photos are automatically processed for face recognition

### Styling

- Modify CSS in the templates directory
- Update Bootstrap classes for different themes
- Customize color schemes in CSS variables

## 🔒 Security

- CSRF protection on all forms
- Input validation and sanitization
- Secure file upload handling
- Admin authentication required for sensitive operations

## 🚀 Deployment

### Production Setup

1. Set `DEBUG = False` in settings.py
2. Configure production database
3. Set up static file serving
4. Configure HTTPS
5. Set up proper logging

### Docker Deployment

```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Contact the development team

---

<div align="center">

**Built with ❤️ for Dr. C.V. Raman University Khandwa**

</div>