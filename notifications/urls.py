from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('admin/', views.admin_notification_dashboard, name='admin_notification_dashboard'),
]