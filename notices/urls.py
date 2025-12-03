from django.urls import path
from . import views

urlpatterns = [
    path('', views.notice_list, name='notice_list'),
    path('create/', views.create_notice, name='create_notice'),

]
