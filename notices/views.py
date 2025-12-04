from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from django.contrib import messages
from django.contrib.auth.models import User
from .models import Notice
from .forms import NoticeForm
from theUsers.models import Profile
from django.core.mail import send_mass_mail

#PUBLICCNOTICE PAGE
def public_notices(request):
    notices = Notice.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'notices/public_notices.html', {'notices': notices})

#LOGGED-IN NOTICE LIST
@login_required
def notice_list(request):
    notices = Notice.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'notices/notice_list.html', {'notices': notices})

#CREATE NOTICE VIEW(FOR STAFF AND ADMIN)
@login_required
def create_notice(request):
    profile = Profile.objects.get(user=request.user)

    if profile.role != 'admin' and profile.role != 'staff':
        messages.error(request, "You are not allowed to post notices.")
        return redirect('notice_list')

    if request.method == 'POST':
        form = NoticeForm(request.POST, request.FILES)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.posted_by = request.user
            notice.save()

            #students = Profile.objects.filter(role='student').values_list('user__id', flat=True)
            #recipients = User.objects.filter(id__in=students, is_active=True)

            messages.success(request, "Notice submitted for approval.")
            return redirect('notice_list')
    else:
        form = NoticeForm()

    return render(request, 'notices/create_notice.html', {'form': form})

@login_required
def notice_list(request):
    notices = Notice.objects.filter(
        approved=True,
        expiry_date__gt=timezone.now()
        ).order_by('-created_at')
    
    return render(request, "notices/notice_list.html", {"notices": notices})

def notice_detail(request, pk):
    notice = get_object_or_404(Notice, pk=pk, approved=True)
    return render(request, 'notices/notice_detail.html', {'notice': notice})


#APPROVE NOTICE VIEW (FOR ADMIN)
@login_required
def approve_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    notice.approved = True
    notice.save()
    return redirect("admin_notice_list")

#ADMIN DASHBOARD TO MANAGE NOTICES
@staff_member_required
def admin_notice_dashboard(request):
    pending_notices = Notice.objects.filter(approved=False)
    active_notices = Notice.objects.filter(approved=True, expiry_date__gt=timezone.now)
    expired_notices = Notice.objects.filter(approved=True, expiry_date__lte=timezone.now)
    approved_notices = Notice.objects.filter(approved=True)
    users =User.objects.count()

    return render(request, 'notices/admin_dashboard.html', {
        'pending_notices': pending_notices,
        'approved_notices': approved_notices,
        'active_notices': active_notices,
        'expired_notices': expired_notices,
        
    })


#APPROVE NOTICE AND SEND NOTIFICATIONS
@staff_member_required
def approve_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    notice.approved = True
    notice.save()

    # Notification content
    title = f"New Notice: {notice.title}"
    message = f"{notice.content[:200]}..."  # short preview
    url = f"/notices/{notice.pk}/"  # a detail view later

    # Notifications for all active users (or filter by role/department)
    from notifications.models import Notification
    recipients = User.objects.filter(is_active=True)
    notifications = []
    for user in recipients:
        notifications.append(Notification(user=user, title=title, message=message, url=url))
    Notification.objects.bulk_create(notifications)

    messages.success(request, "Notice approved and notifications sent!")
    return redirect('admin_notice_dashboard')


"""
    # Comment out if you don't want emails.
    if getattr(settings, 'SEND_EMAIL_ON_NOTICE', False):
        emails = [u.email for u in recipients if u.email]
        # send a simple email — for many users use batching or background tasks
        send_mail(
            subject=title,
            message=notice.content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=emails,
            fail_silently=True
        )
"""

    


@staff_member_required
def reject_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    notice.delete()
    messages.warning(request, "Notice rejected and deleted.")
    return redirect('admin_notice_dashboard')


def public_notices(request):
    notices = Notice.objects.filter(
        approved=True,
        expiry_date__gt=timezone.now()
        ).order_by('-created_at')
    
    return render(request, 'notices/public_notices.html', {'notices': notices})

@login_required
def download_notice_file(request, pk):
    notice = get_object_or_404(Notice, pk=pk, approved=True)
    return redirect(notice.attachment.url)
