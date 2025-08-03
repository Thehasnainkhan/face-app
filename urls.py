from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('export/', views.export_excel, name='export'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('delete_student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('delete_attendance/<int:attendance_id>/', views.delete_attendance, name='delete_attendance'),
    path('reset_database/', views.reset_database, name='reset_database'),
    path('register/', views.register, name='register'),
]