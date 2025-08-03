from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
import json
import base64
import cv2
import numpy as np
import os
import pandas as pd
from .models import Student, Attendance
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import io
from PIL import Image

# Google Sheets setup (you'll need to add your credentials)
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def get_google_sheets_client():
    """Get Google Sheets client for attendance tracking"""
    try:
        # You'll need to add your credentials.json file
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            'credentials.json', SCOPES)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"Google Sheets error: {e}")
        return None

def home(request):
    """Home page with webcam interface"""
    return render(request, 'home.html')

@csrf_exempt
def upload_image(request):
    """Handle image upload and face recognition"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data['image'].split(',')[1]
            img_bytes = base64.b64decode(image_data)
            
            # Convert to OpenCV format
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Use real face recognition
            from .face_utils import recognize_face
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            known_faces_dir = os.path.join(base_dir, 'known_faces')
            student_id, recog_info = recognize_face(img, known_faces_dir)
            today = timezone.now().date()
            if student_id:
                # Try to find student by student_id
                student = Student.objects.filter(student_id=student_id).first()
                if not student:
                    # If not found, create a new student with this ID
                    student = Student.objects.create(
                        name=student_id,
                        student_id=student_id
                    )
                existing_attendance = Attendance.objects.filter(
                    student=student,
                    date=today
                ).first()
                if not existing_attendance:
                    attendance = Attendance.objects.create(
                        student=student,
                        date=today,
                        status='present'
                    )
                    # Try to save to Google Sheets
                    try:
                        client = get_google_sheets_client()
                        if client:
                            sheet = client.open('Attendance Sheet').sheet1
                            sheet.append_row([student.name, today.strftime('%Y-%m-%d'), timezone.now().strftime('%H:%M:%S')])
                    except Exception as e:
                        print(f"Google Sheets error: {e}")
                    return JsonResponse({
                        'success': True,
                        'message': f"{student.name}'s attendance marked successfully!"
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': f"{student.name}'s attendance already marked today."
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'message': f"Face not recognized: {recog_info}"
                })
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f"Error processing image: {str(e)}"
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def dashboard(request):
    """Admin dashboard to view attendance"""
    # Get filter parameters
    date_filter = request.GET.get('date', '')
    name_filter = request.GET.get('name', '')
    month_filter = request.GET.get('month', '')
    
    # Get attendance records
    attendance_list = Attendance.objects.select_related('student').all().order_by('-date', '-time_in')
    
    # Apply filters
    if date_filter:
        attendance_list = attendance_list.filter(date=date_filter)
    
    if name_filter:
        attendance_list = attendance_list.filter(student__name__icontains=name_filter)
    
    if month_filter:
        year, month = month_filter.split('-')
        attendance_list = attendance_list.filter(date__year=year, date__month=month)
    
    # Get unique dates for filter dropdown
    dates = Attendance.objects.values_list('date', flat=True).distinct().order_by('-date')
    
    # Get unique students for filter dropdown
    students = Student.objects.all().order_by('name')
    
    # Get all registered students for the students table
    all_students = Student.objects.all().order_by('name')
    
    # Count late students today
    today = timezone.now().date()
    late_count = Attendance.objects.filter(date=today, status='Late').count()
    
    context = {
        'attendance_list': attendance_list,
        'dates': dates,
        'students': students,
        'all_students': all_students,
        'date_filter': date_filter,
        'name_filter': name_filter,
        'month_filter': month_filter,
        'late_count': late_count,
    }
    
    return render(request, 'dashboard.html', context)

def export_excel(request):
    """Export attendance data to Excel"""
    export_type = request.GET.get('type', 'all')
    date_value = request.GET.get('date', '')
    month_value = request.GET.get('month', '')
    
    # Get attendance data based on export type
    if export_type == 'date' and date_value:
        attendance_list = Attendance.objects.filter(date=date_value)
    elif export_type == 'month' and month_value:
        year, month = month_value.split('-')
        attendance_list = Attendance.objects.filter(date__year=year, date__month=month)
    else:
        attendance_list = Attendance.objects.all()
    
    # Create DataFrame
    data = []
    for attendance in attendance_list:
        data.append({
            'Student Name': getattr(attendance.student, 'name', ''),
            'Student ID': getattr(attendance.student, 'student_id', ''),
            'Date': attendance.date.strftime('%Y-%m-%d') if attendance.date else '',
            'Time In': attendance.time_in.strftime('%H:%M:%S') if attendance.time_in else '',
            'Status': attendance.status if attendance.status else '',
        })

    # If no records, add a note row
    if not data:
        data.append({
            'Student Name': 'No attendance records found',
            'Student ID': '',
            'Date': '',
            'Time In': '',
            'Status': ''
        })

    df = pd.DataFrame(data)

    # Create Excel file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Attendance', index=False)
    output.seek(0)

    # Create response
    filename = f"attendance_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    response = HttpResponse(
        output.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response

def chatbot(request):
    """LLM-powered assistant for attendance analysis, logs Q&A, summarizes all data"""
    import traceback
    from openai import OpenAI
    from django.conf import settings
    from .models import Attendance, Student, ChatHistory
    from django.utils import timezone

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_query = data.get('query', '').strip().lower()

            # Database-driven Q&A for common attendance questions
            from django.db.models import Count
            db_answer = None
            if 'total present' in user_query or 'how many present' in user_query:
                total_present = Attendance.objects.filter(status='present').count()
                db_answer = f"Total present: {total_present}"
            elif 'most absent' in user_query or 'most absences' in user_query:
                absent_counts = (Attendance.objects.filter(status='absent')
                    .values('student__name')
                    .annotate(total=Count('id'))
                    .order_by('-total'))
                if absent_counts:
                    max_absent = absent_counts[0]['total']
                    most_absent = [a['student__name'] for a in absent_counts if a['total'] == max_absent]
                    db_answer = f"Most absent: {', '.join(most_absent)} ({max_absent} absences)"
                else:
                    db_answer = "No absences recorded."
            elif 'total absent' in user_query or 'how many absent' in user_query:
                total_absent = Attendance.objects.filter(status='absent').count()
                db_answer = f"Total absent: {total_absent}"
            elif 'total late' in user_query or 'how many late' in user_query:
                total_late = Attendance.objects.filter(status='late').count()
                db_answer = f"Total late: {total_late}"
            # Add more database-driven Q&A as needed

            if db_answer:
                ChatHistory.objects.create(question=user_query, answer=db_answer)
                return JsonResponse({'response': db_answer})

            # --- LLM fallback for complex/natural questions ---
            # Summarize all attendance data for context
            all_records = Attendance.objects.select_related('student').all()
            total_attendance = all_records.count()
            unique_students = Student.objects.count()
            date_range = (all_records.order_by('date').first(), all_records.order_by('-date').first()) if total_attendance else (None, None)
            status_counts = all_records.values('status').order_by().annotate(count=models.Count('status'))
            status_summary = ', '.join([f"{s['status']}: {s['count']}" for s in status_counts]) if status_counts else 'No records.'

            summary = f"Total records: {total_attendance}, Unique students: {unique_students}, Status breakdown: {status_summary}."
            if date_range[0] and date_range[1]:
                summary += f" Date range: {date_range[0].date} to {date_range[1].date}."

            # Gather recent attendance records (for detailed context)
            attendance_records = all_records.order_by('-date', '-time_in')[:100]
            records = []
            for att in attendance_records:
                records.append({
                    'Student Name': att.student.name,
                    'Student ID': att.student.student_id,
                    'Date': att.date.strftime('%Y-%m-%d') if att.date else '',
                    'Time In': att.time_in.strftime('%H:%M:%S') if att.time_in else '',
                    'Status': att.status if att.status else '',
                })
            data_table = '\n'.join([
                f"{r['Student Name']} | {r['Student ID']} | {r['Date']} | {r['Time In']} | {r['Status']}" for r in records
            ])

            prompt = f"""
You are an attendance assistant for a school. Here is a summary of all attendance data:
{summary}

Here are the most recent attendance records (table):
Student Name | Student ID | Date | Time In | Status
{data_table}

A user asked: '{user_query}'

Based on the summary and the data above, answer the question as helpfully as possible. If the answer requires calculation or listing, do so. If you can't answer from the data, say so politely.
"""

            # Get OpenAI API key from Django settings
            api_key = getattr(settings, 'OPENAI_API_KEY', None)
            if not api_key:
                return JsonResponse({'response': 'OpenAI API key not set. Please configure OPENAI_API_KEY in settings.'})
            client = OpenAI(api_key=api_key)

            # Call GPT-4o
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": "You are a helpful assistant for attendance analytics."},
                          {"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.2
            )
            answer = response.choices[0].message.content.strip()

            # Log Q&A to ChatHistory
            ChatHistory.objects.create(question=user_query, answer=answer)

            return JsonResponse({'response': answer})
        except Exception as e:
            import logging
            tb = traceback.format_exc()
            logging.error(f"Chatbot error: {tb}")
            # Always return valid JSON
            return JsonResponse({'response': 'Sorry, I encountered an internal error. Please contact admin or try again later.'}, status=500)
    return JsonResponse({'response': 'Invalid request'}, status=400)

# Export chat history as CSV
from django.http import StreamingHttpResponse
import csv

def export_chat_history(request):
    """Export chat Q&A log as CSV"""
    rows = ChatHistory.objects.order_by('-timestamp').all()
    def row_iter():
        yield ['Timestamp', 'Question', 'Answer']
        for r in rows:
            yield [r.timestamp.strftime('%Y-%m-%d %H:%M:%S'), r.question, r.answer]
    response = StreamingHttpResponse((csv.writer(response := io.StringIO()).writerow(row) or response.getvalue() for row in row_iter()), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="chat_history.csv"'
    return response


def delete_student(request, student_id):
    """Delete a student and all their attendance records"""
    try:
        student = Student.objects.get(id=student_id)
        student_name = student.name
        student.delete()
        messages.success(request, f"Student {student_name} has been deleted successfully.")
    except Student.DoesNotExist:
        messages.error(request, "Student not found.")
    except Exception as e:
        messages.error(request, f"Error deleting student: {str(e)}")
    
    return redirect('dashboard')

def delete_attendance(request, attendance_id):
    """Delete an attendance record"""
    try:
        attendance = Attendance.objects.get(id=attendance_id)
        student_name = attendance.student.name
        date = attendance.date
        attendance.delete()
        messages.success(request, f"Attendance record for {student_name} on {date} has been deleted successfully.")
    except Attendance.DoesNotExist:
        messages.error(request, "Attendance record not found.")
    except Exception as e:
        messages.error(request, f"Error deleting attendance record: {str(e)}")
    
    return redirect('dashboard')

def reset_database(request):
    """Reset the entire database (delete all students and attendance records)"""
    if request.method == 'POST':
        try:
            # Delete all attendance records first
            attendance_count = Attendance.objects.all().count()
            Attendance.objects.all().delete()
            
            # Delete all students and their photos
            student_count = Student.objects.all().count()
            
            # Delete student photos from known_faces directory
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            known_faces_dir = os.path.join(base_dir, 'known_faces')
            for filename in os.listdir(known_faces_dir):
                if filename.endswith('.jpeg') or filename.endswith('.jpg') or filename.endswith('.png'):
                    try:
                        os.remove(os.path.join(known_faces_dir, filename))
                    except Exception as e:
                        print(f"Error deleting file {filename}: {e}")
            
            # Delete all students from database
            Student.objects.all().delete()
            
            messages.success(request, f"Successfully reset database: deleted {attendance_count} attendance records and {student_count} students.")
        except Exception as e:
            messages.error(request, f"Error resetting database: {str(e)}")
    
    return redirect('dashboard')

def register(request):
    """Register a new student"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            student_id = request.POST.get('student_id')
            email = request.POST.get('email', '')
            photo = request.FILES.get('photo')
            
            if not name or not student_id:
                messages.error(request, "Name and Student ID are required.")
                return redirect('register')
            
            # Check if student with this ID already exists
            if Student.objects.filter(student_id=student_id).exists():
                messages.error(request, f"Student with ID {student_id} already exists.")
                return redirect('register')
            
            # Create new student
            student = Student.objects.create(
                name=name,
                student_id=student_id,
                email=email,
                photo=photo
            )

            # Save photo to known_faces for recognition
            if photo:
                try:
                    from .face_utils import save_student_photo
                    from PIL import Image
                    import io
                    photo.seek(0)
                    img = Image.open(photo)
                    save_student_photo(img, student_id)
                except Exception as e:
                    print(f"Error saving photo to known_faces: {e}")
            
            messages.success(request, f"Student {name} has been registered successfully! They can now mark attendance using the face recognition system.")
            return redirect('dashboard')
            
        except Exception as e:
            messages.error(request, f"Error registering student: {str(e)}")
    
    # For GET requests, just render the registration form
    return render(request, 'register.html')
