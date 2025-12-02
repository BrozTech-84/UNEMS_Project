from django.db import models
from django.contrib.auth.models import User
from events.models import Event

# Create your models here.

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)

    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)
    merchant_request_id = models.CharField(max_length=100, blank=True, null=True)

    status = models.CharField(max_length=50, default='Pending')  # Success/Failed/Pending
    transaction_code = models.CharField(max_length=20, blank=True, null=True)

    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"


class MPesaCallbackData(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='callback_data')
    raw_response = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Callback for Payment {self.payment.id}"
