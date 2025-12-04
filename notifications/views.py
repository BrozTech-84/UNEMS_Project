from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.http import JsonResponse

@login_required
def notification_list(request):
    notes = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications/list.html', {'notifications': notes})

@login_required
def mark_as_read(request):
    # expects POST with 'id'
    if request.method == 'POST':
        nid = request.POST.get('id')
        try:
            note = Notification.objects.get(id=nid, user=request.user)
            note.is_read = True
            note.save()
            return JsonResponse({'status': 'ok'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error'}, status=404)
    return JsonResponse({'status': 'invalid'}, status=400)
