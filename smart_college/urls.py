from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Includes login and other core views
    path('student/dashboard/', include('studentdash.urls')),
    path('staff/dashboard/', include('staffdash.urls')),  # Add this line for staff dashboard
]