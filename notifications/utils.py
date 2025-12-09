from django.core.mail import send_mail
from django.contrib.auth.models import User
from .models import Notification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

def notify_all_users(subject, message):
    users = User.objects.all()

    for user in users:
        # Save in-app notification
        Notification.objects.create(
            user=user,
            message=message
        )

        # Send email if user has an email
        if user.email:
            send_mail(
                subject,
                message,
                'admin@university.com',  # sender email
                [user.email],
                fail_silently=True,
            )

         # WebSocket push
        async_to_sync(channel_layer.group_send)(
            f"user_{user.id}",
            {
                "type": "send_notification",
                "message": notification.message,
                "created_at": notification.created_at.strftime("%Y-%m-%d %H:%M"),
            }
        )
