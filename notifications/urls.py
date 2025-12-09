from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin_notification_dashboard, name='admin_notification_dashboard'),
    path('my/', views.user_notifications, name='user_notifications'),
    path('mark-read/<int:pk>/', views.mark_notification_read, name='mark_notification_read'),
    path('mark-all-read/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
]
