from django.urls import path
from . import views

urlpatterns = [
    path('', views.notice_list, name='notice_list'),
    path('public/', views.public_notices, name='public_notices'),

    path('create/', views.create_notice, name='create_notice'),
    path('<int:pk>/', views.notice_detail, name='notice_detail'),
    path('download/<int:pk>/', views.download_notice_file, name='download_notice'),


    # Admin Dashboard
    path('admin/dashboard/', views.admin_notice_dashboard, name='admin_notice_dashboard'),
    

    # Approve & Reject (Admin Only)
    path('admin/approve/<int:notice_id>/', views.approve_notice, name='approve_notice'),
    path('admin/reject/<int:notice_id>/', views.reject_notice, name='reject_notice'),
]
