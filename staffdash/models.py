from django.db import models
from django.conf import settings  # Add this import

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    roll_no = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    class_name = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.full_name} ({self.roll_no})"

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('late', 'Late'),
        ('absent', 'Absent'),
    ]
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        unique_together = ('student', 'date')
    
    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"