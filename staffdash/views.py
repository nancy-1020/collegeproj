from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Student, Attendance
from datetime import date

User = get_user_model()

@login_required
def staff_dashboard(request):
    
    if not request.user.role == 'staff':
        messages.error(request, "You don't have permission to access this page")
        return redirect('home')  # Redirect to appropriate page
    
    today = date.today()
    attendance_data = Attendance.objects.filter(date=today).select_related('student')
    students = Student.objects.all()
    
    # Calculate stats
    total_students = Student.objects.count()
    present_count = Attendance.objects.filter(date=today, status='present').count()
    late_count = Attendance.objects.filter(date=today, status='late').count()
    absent_count = Attendance.objects.filter(date=today, status='absent').count()
    
    try:
        attendance_percentage = round((present_count + late_count) / total_students * 100, 2)
    except ZeroDivisionError:
        attendance_percentage = 0
    
    context = {
        'today': today.strftime("%B %d, %Y"),
        'attendance_data': attendance_data,
        'students': students,
        'stats': {
            'total_students': total_students,
            'attendance_percentage': attendance_percentage,
            'present_count': present_count,
            'late_count': late_count,
            'absent_count': absent_count,
        },
        'teacher_id': request.user.teacher_id  # Add teacher ID to context
    }
    return render(request, 'staffdash/dashboard.html', context)

@login_required
def mark_attendance(request):
    if not request.user.role == 'staff':
        messages.error(request, "Unauthorized access")
        return redirect('home')
        
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        try:
            student = Student.objects.get(id=student_id)
            Attendance.objects.update_or_create(
                student=student,
                date=date.today(),
                defaults={
                    'status': status,
                    'notes': notes,
                    'marked_by': request.user
                }
            )
            messages.success(request, f"Attendance marked successfully for {student.full_name}!")
        except Exception as e:
            messages.error(request, f"Error marking attendance: {str(e)}")
    
    return redirect('staff_dashboard')