from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date
from attendance.models import Attendance

@login_required
def student_dashboard(request):
    user = request.user
    today = date.today()

    # Today's status
    try:
        today_status = Attendance.objects.get(student=user, date=today).status
    except Attendance.DoesNotExist:
        today_status = "Not Marked"

    # All attendance records of this student
    all_attendance = Attendance.objects.filter(student=user)
    total_days = all_attendance.count()
    present_days = all_attendance.filter(status='present').count()

    # Attendance percentage
    attendance_percentage = round((present_days / total_days) * 100) if total_days > 0 else 0

    context = {
        'today_status': today_status.capitalize(),
        'present_days': present_days,
        'total_days': total_days,
        'attendance_percentage': attendance_percentage,
        'minimum_required': 75,
    }

    return render(request, 'studentdash/dashboard.html', context)
