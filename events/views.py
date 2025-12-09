from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required, user_passes_test
from django.contrib import messages
from .forms import EventForm
from .models import Event, EventRegistration, EventAttendance
from django.conf import settings
from .models import EventPayment
from django.urls import reverse
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
from django.http import JsonResponse
import requests
import base64
from datetime import datetime

#------------------------
#HELPER: ADMIN CHECK
#-------------------------
def is_admin(user):
    return user.is_superuser or user.is_staff

def index(request):
    cl = MpesaClient()
    # Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
    phone_number = '0792729050'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://api.darajambili.com/express-payment'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)

# PUBLIC EVENTS LIST
@login_required
def event_list(request):
    events = Event.objects.order_by('-date')
    return render(request, 'events/event_list.html', {'events': events})

# REGISTER FOR EVENT
@login_required
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if EventRegistration.objects.filter(event=event, student=request.user).exists():
        messages.warning(request, "You are already registered for this event.")
        return redirect('event_list')

    EventRegistration.objects.create(event=event, student=request.user)
    messages.success(request, "You have successfully registered for the event.")
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
    return redirect('admin_dashboard')

# INITIATING PAYMENT VIA MPESAclient

@login_required
def initiate_payment(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    # Check if event requires payment
    if not event.is_paid:
        messages.error(request, "This event does not require payment.")
        return redirect('event_list')

    if request.method == 'POST':
        phone = request.POST.get('phone')

        if not phone:
            messages.error(request, "Enter phone number.")
            return redirect('initiate_payment', event_id=event.id)

        # ✅ Normalize phone number
        if phone.startswith('0'):
            phone = '254' + phone[1:]
        elif phone.startswith('+'):
            phone = phone[1:]

        cl = MpesaClient()
        amount = int(event.price)
        account_reference = f"EVENT{event.id}"
        transaction_desc = f"Payment for {event.title}"

        # ✅ CALLBACK URL 
        callback_url = "https://bette-gnarly-cain.ngrok-free.dev/events/mpesa/callback/"

        try:
            response = cl.stk_push(
                phone,
                amount,
                account_reference,
                transaction_desc,
                callback_url
            )
            print("FULL MPESA RESPONSE:", vars(response))


            # ✅ RESPONSE ACCESS
            checkout_id = response.checkout_request_id
            response_code = response.response_code
            response_desc = response.response_description

            if response_code == '0':
                # ✅ SAVE PAYMENT 
                EventPayment.objects.create(
                    event=event,
                    user=request.user,
                    amount=amount,
                    phone_number=phone,
                    mpesa_checkout_request_id=checkout_id,
                    status=EventPayment.PENDING
                )

                messages.success(request, "Payment request sent. Enter your M-Pesa PIN.")

            else:
                messages.error(request, f"Mpesa Error: {response_desc}")

        except Exception as e:
            messages.error(request, f"Payment failed: {e}")

        return redirect('my_events')

    return render(request, 'events/initiate_payment.html', {'event': event})

# -------------------------------
# MPESA CALLBACK URL (REQUIRED)
# -------------------------------
@csrf_exempt
def mpesa_callback(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))

        print("✅ MPESA CALLBACK DATA:", data)

        try:
            stk_callback = data['Body']['stkCallback']
            result_code = stk_callback['ResultCode']
            checkout_id = stk_callback['CheckoutRequestID']

            payment = EventPayment.objects.get(
                mpesa_checkout_request_id=checkout_id
            )

            if result_code == 0:
                payment.status = EventPayment.SUCCESS
                payment.mpesa_transaction_id = stk_callback.get('MpesaReceiptNumber', '')
                payment.save()

                # ✅ Mark registration as paid
                EventRegistration.objects.filter(
                    event=payment.event,
                    student=payment.user
                ).update(has_paid=True)

            else:
                payment.status = EventPayment.FAILED
                payment.save()

        except Exception as e:
            print("❌ CALLBACK ERROR:", str(e))

        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

    return JsonResponse({"error": "Invalid request"}, status=400)
