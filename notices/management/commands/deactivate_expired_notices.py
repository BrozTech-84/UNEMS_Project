# notices/management/commands/deactivate_expired_notices.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from notices.models import Notice

class Command(BaseCommand):
    help = "Deactivate notices whose expiry_date has passed"

    def handle(self, *args, **options):
        today = timezone.localdate()
        expired_qs = Notice.objects.filter(is_active=True, expiry_date__lt=today)
        count = expired_qs.count()
        if count == 0:
            self.stdout.write("No expired notices to deactivate.")
            return
        expired_qs.update(is_active=False)
        self.stdout.write(f"Deactivated {count} expired notices.")
