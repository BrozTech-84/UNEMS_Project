from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notice
from .forms import NoticeForm
from theUsers.models import Profile
from django.contrib.admin.views.decorators import staff_member_required


@login_required
def notice_list(request):
    notices = Notice.objects.filter(approved=True).order_by('-created_at')
    return render(request, 'notices/notice_list.html', {'notices': notices})


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
            messages.success(request, "Notice submitted for approval.")
            return redirect('notice_list')
    else:
        form = NoticeForm()

    return render(request, 'notices/create_notice.html', {'form': form})

@login_required
def notice_list(request):
    notices = Notice.objects.filter(approved=True).order_by('-created_at')
    return render(request, "notices/notice_list.html", {"notices": notices})


@login_required
def approve_notice(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    notice.approved = True
    notice.save()
    return redirect("admin_notice_list")

@staff_member_required
def admin_notice_dashboard(request):
    pending_notices = Notice.objects.filter(approved=False)
    approved_notices = Notice.objects.filter(approved=True)

    return render(request, 'notices/admin_dashboard.html', {
        'pending_notices': pending_notices,
        'approved_notices': approved_notices
    })


@staff_member_required
def approve_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    notice.approved = True
    notice.save()
    messages.success(request, "Notice approved successfully!")
    return redirect('admin_notice_dashboard')


@staff_member_required
def reject_notice(request, notice_id):
    notice = get_object_or_404(Notice, id=notice_id)
    notice.delete()
    messages.warning(request, "Notice rejected and deleted.")
    return redirect('admin_notice_dashboard')