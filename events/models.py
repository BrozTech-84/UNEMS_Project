from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    venue = models.CharField(max_length=255)
    date = models.DateTimeField()
    time = models.TimeField(default="09:00")
    organizer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='organized_events')
    poster = models.ImageField(upload_to='events/', blank=True, null=True)
    
    is_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.title
    

class EventRegistration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    registered_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    has_paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('event', 'student')

    def __str__(self):
        return f"{self.student} -> {self.event.title}"
    
    # Payment Details
class EventPayment(models.Model):
    PENDING = 'PENDING'
    SUCCESS = 'SUCCESS'
    FAILED = 'FAILED'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (SUCCESS, 'Success'),
        (FAILED, 'Failed'),
    ]

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='payments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    phone_number = models.CharField(max_length=20)
    mpesa_checkout_request_id = models.CharField(max_length=255, blank=True, null=True)
    mpesa_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        indexes = [
            models.Index(fields=['mpesa_checkout_request_id']),
            models.Index(fields=['mpesa_transaction_id']),
        ]
        constraints = [
            models.UniqueConstraint(
            fields=['mpesa_checkout_request_id'],
            name='unique_mpesa_checkout_request'
            )
        ]


    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.status}"

def mark_paid(self):
    self.has_paid = True
    self.save()


class EventAttendance(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)
    marked_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student.username} - {self.event.title} - {self.attended}"
