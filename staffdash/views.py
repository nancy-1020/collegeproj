from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
# from .models import  Attendance
from attendance.models import Attendance

from datetime import date

User = get_user_model()

# --------------------------
# Staff Dashboard View
# --------------------------

@login_required
def staff_dashboard(request):
    if request.user.role != 'staff':
        messages.error(request, "You don't have permission to access this page")
        return redirect('home')

    today = date.today()

    # ✅ Use Student model, not User model
    students = User.objects.filter(role='student') 
    attendance_data = Attendance.objects.filter(date=today).select_related('student')

    # ✅ Accurate stats
    total_students = students.count()
    present_count = Attendance.objects.filter(date=today, status='Present').count()
    late_count = Attendance.objects.filter(date=today, status='Late').count()
    absent_count = Attendance.objects.filter(date=today, status='Absent').count()

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
        'teacher_id': request.user.teacher_id,
    }

    return render(request, 'staffdash/dashboard.html', context)

# --------------------------
@login_required
def mark_attendance(request):
    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        status = request.POST.get('status')
       

        try:
            # ❌ Wrong: student = Student.objects.get(id=student_id)
            # ✅ Correct:
            student = User.objects.get(id=student_id)

            # Avoid duplicate entries for the same day
            attendance, created = Attendance.objects.get_or_create(
                student=student,
                date=date.today(),
                defaults={'status': status}
            )
            if not created:
                attendance.status = status
                
                attendance.save()

            messages.success(request, 'Attendance marked successfully!')
        except User.DoesNotExist:
            messages.error(request, 'Student not found.')
        
        return redirect('staff_dashboard')
    
    # For GET request, show the form
    students = User.objects.filter(role='student')
    return render(request, 'staffdash/mark_attendance.html', {'students': students})
