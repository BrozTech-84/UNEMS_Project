from django.urls import path
from . import views

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('register/<int:event_id>/', views.register_event, name='register_event'),


    # Admin
    path('admin/dashboard/', views.admin_event_dashboard, name='admin_event_dashboard'),
    path('admin/delete/<int:event_id>/', views.delete_event, name='delete_event'),
    path('admin/create/', views.create_event, name='create_event'),
    path('admin/events/', views.event_list, name='event_list'),
    path('admin/registrations/', views.admin_event_registrations, name='admin_event_registrations'),
    path('admin/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    
    # Student
    path('my-events/', views.my_events, name='my_events'),
    path('index/', views.index, name='index'),
    path('pay/<int:event_id>/', views.initiate_payment, name='initiate_payment'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),

    # Attendance
    path('admin/attendance/<int:pk>/<int:student_id>/', views.mark_attendance, name='mark_attendance'),
]

