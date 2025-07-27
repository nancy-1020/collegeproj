from django.db import models
from django.conf import settings
from datetime import date
from core.models import CustomUser
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('late', 'Late'),
        ('absent', 'Absent'),
    ]
    
    student = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='attendances_as_student'
    )
    marked_by = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='attendances_marked_by',
         null=True
    )
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"


