from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import LoginForm
from core.models import CustomUser as User
from django.contrib.auth import logout

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            password = form.cleaned_data.get('password')

            if role == 'student':
                roll_no = form.cleaned_data.get('roll_number')
                user = User.objects.filter(roll_no=roll_no, role='student').first()
                if user:
                    auth_user = authenticate(request, email=user.email, password=password)
                    if auth_user:
                        login(request, auth_user)
                        return redirect('student_dashboard')
                    else:
                        messages.error(request, "Incorrect password")
                else:
                    messages.error(request, "Student not found with provided roll number")

            elif role == 'staff':
                teacher_id = form.cleaned_data.get('teacher_id')
                user = User.objects.filter(teacher_id=teacher_id, role='staff').first()
                if user:
                    auth_user = authenticate(request, email=user.email, password=password)
                    if auth_user:
                        login(request, auth_user)
                        return redirect('staff_dashboard')
                    else:
                        messages.error(request, "Incorrect password")
                else:
                    messages.error(request, "Staff not found with provided teacher ID")

            elif role == 'admin':
                return redirect('/admin/')
        else:
            messages.error(request, "Form is invalid")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
     logout(request)
     return redirect('login') 
