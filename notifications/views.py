from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def notification_list(request):
    return HttpResponse("Notifications app is working!")
