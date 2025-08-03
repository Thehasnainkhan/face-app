from django.contrib import admin
from .models import Student, Attendance

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'student_id', 'email', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'student_id', 'email')
    ordering = ('name',)
    readonly_fields = ('created_at',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'time_in', 'status')
    list_filter = ('date', 'status', 'student')
    search_fields = ('student__name', 'student__student_id')
    ordering = ('-date', '-time_in')
    readonly_fields = ('created_at',)
    date_hierarchy = 'date'
