from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('register/<int:event_id>/', views.register_event, name='register_event'),

    # Admin
    path('admin/dashboard/', views.admin_event_dashboard, name='admin_event_dashboard'),
    path('admin/attendance/<int:event_id>/<int:student_id>/', views.mark_attendance, name='mark_attendance'),
    
    # Student
    path('register/<int:pk>/', views.register_event, name='register_event'),

    # Attendance
    path('admin/attendance/<int:pk>/<int:student_id>/', views.mark_attendance, name='mark_attendance'),
]

