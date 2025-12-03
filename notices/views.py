from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notice
from .forms import NoticeForm
from theUsers.models import Profile

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
