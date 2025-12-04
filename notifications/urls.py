from django.urls import path
from . import views

urlpatterns = [
    path('', views.notification_list, name='notification_list'),
    path('mark-read/', views.mark_as_read, name='notification_mark_as_read'),

]
