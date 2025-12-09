from django.urls import path
from . import views

urlpatterns = [
    # Public / Student
    path('', views.event_list, name='event_list'),
    path('register/<int:event_id>/', views.register_event, name='register_event'),
    path('my-events/', views.my_events, name='my_events'),
    path('index/', views.index, name='index'),
    path('pay/<int:event_id>/', views.initiate_payment, name='initiate_payment'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),

    # Admin Dashboard
    path('admin/dashboard/', views.admin_event_dashboard, name='admin_event_dashboard'),

    # Admin Event Management
    path('admin/events/', views.event_list, name='admin_event_list'),
    path('admin/create/', views.create_event, name='create_event'),
    path('admin/edit/<int:event_id>/', views.edit_event, name='edit_event'),
    path('admin/delete/<int:event_id>/', views.delete_event, name='delete_event'),

    # Admin Registrations
    path('admin/registrations/', views.admin_event_registrations, name='admin_event_registrations'),

    # Admin Attendance
    path('admin/attendance/<int:pk>/<int:student_id>/', views.mark_attendance, name='mark_attendance'),
]

