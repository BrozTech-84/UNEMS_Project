from django.urls import path
from . import views

urlpatterns = [
    path('', views.notice_list, name='notice_list'),
    path('create/', views.create_notice, name='create_notice'),
    path("approve/<int:pk>/", views.approve_notice, name="approve_notice"),
    path('admin/dashboard/', views.admin_notice_dashboard, name='admin_notice_dashboard'),
    path('admin/approve/<int:notice_id>/', views.approve_notice, name='approve_notice'),
    path('admin/reject/<int:notice_id>/', views.reject_notice, name='reject_notice'),
]
