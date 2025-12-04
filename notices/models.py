from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Notice(models.Model):
    CATEGORY_CHOICES = (
    ('general', 'General'),
    ('academic', 'Academic'),
    ('exams', 'Examinations'),
    ('clubs', 'Clubs'),
    ('hostels', 'Hostels'),
)

    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    attachment = models.FileField(upload_to='notices/', blank=True, null=True)
    posted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='notice_author')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)

    expiry_date = models.DateTimeField(null=True, blank=True)

    def is_expired(self):
        if self.expiry_date:
            return timezone.now() > self.expiry_date
        return False
    
    def __str__(self):
        return self.title
