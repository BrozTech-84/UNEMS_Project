from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def notice_list(request):
    return HttpResponse("Notices app is working!")
