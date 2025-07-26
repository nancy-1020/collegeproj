from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import date

@login_required
def dashboard(request):
    user = request.user

    # Mock data for now — later connect with Attendance model
    present_days = 42
    total_days = 50
    attendance_percent = round((present_days / total_days) * 100, 2)
    
    # Temporary logic: today is present if date is even, else absent
    today_status = "Present" if date.today().day % 2 == 0 else "Absent"

    context = {
        'user': user,
        'present_days': present_days,
        'total_days': total_days,
        'attendance_percent': attendance_percent,
        'today_status': today_status
    }

    return render(request, 'student/dashboard.html', context)
