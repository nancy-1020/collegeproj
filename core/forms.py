from django import forms

class LoginForm(forms.Form):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    roll_number = forms.CharField(required=False)
    teacher_id = forms.CharField(required=False)
    password = forms.CharField(widget=forms.PasswordInput)
