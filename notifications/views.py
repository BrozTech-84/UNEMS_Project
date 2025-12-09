from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Notification
from django.http import JsonResponse

@login_required
def user_notifications(request):
    notifications = Notification.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'notifications/user_notifications.html', {
        'notifications': notifications
    })

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


@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('user_notifications')

@login_required
def mark_all_notifications_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return redirect('user_notifications')


@staff_member_required
def admin_notification_dashboard(request):
    notification = Notification.objects.all().order_by('-created_at')
    return render(request, 'notifications/admin_dashboard.html', {'notifications': notification})