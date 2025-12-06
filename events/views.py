from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from django.contrib import messages
from .forms import EventForm
from .models import Event, EventRegistration, EventAttendance

#------------------------
#HELPER: ADMIN CHECK
#-------------------------
def is_admin(user):
    return user.is_superuser or user.is_staff

# PUBLIC EVENTS LIST
@login_required
def event_list(request):
    events = Event.objects.order_by('-date')
    return render(request, 'events/event_list.html', {'events': events})

# REGISTER FOR EVENT
@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    obj, created = EventRegistration.objects.get_or_create(
        student=request.user,
        event=event
    )

     # Check if user already registered
    if EventRegistration.objects.filter(event=event, student=request.user).exists():
        messages.warning(request, "You have already registered for this event.")
        return redirect('event_list')

    EventRegistration.objects.create(event=event, student=request.user)
    messages.success(request, "successfully registered for the event.")
    return redirect('event_list')

#  Admin Create Event
@staff_member_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()
            messages.success(request, 'Event created successfully.')
            return redirect('admin_event_dashboard')
    else:
        form = EventForm()

    return render(request, 'events/create_event.html', {'form': form})


# My Registered Events (student dashboard)
@login_required
def my_events(request):
    registrations = EventRegistration.objects.filter(student=request.user)
    return render(request, 'events/my_events.html', {'registrations': registrations})


# ADMIN DASHBOARD
@staff_member_required
def admin_event_dashboard(request):
    events = Event.objects.all()
    return render(request, 'events/admin_dashboard.html', {'events': events})


# MARK ATTENDANCE
@staff_member_required
def mark_attendance(request, event_id, student_id):
    attendance, created = EventAttendance.objects.get_or_create(
        event_id=event_id,
        student_id=student_id
    )
    attendance.attended = True
    attendance.save()

    messages.success(request, "Attendance marked!")
    return redirect('admin_event_dashboard')

@staff_member_required
def admin_event_registrations(request):
    registrations = EventRegistration.objects.select_related('event', 'student')
    return render(request, 'events/admin_event_registrations.html', {
        'registrations': registrations
    })

#  EDIT EVENT (ADMIN)
@login_required
@user_passes_test(is_admin)
def edit_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, "Event updated successfully.")
            return redirect('events_list')
    else:
        form = EventForm(instance=event)

    return render(request, 'events/edit_event.html', {'form': form})


def is_admin(user):
    return user.is_superuser or user.is_staff

@user_passes_test(is_admin)
def delete_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.delete()
    messages.success(request, "Event deleted successfully.")
    return redirect('admin_dashboard.html')