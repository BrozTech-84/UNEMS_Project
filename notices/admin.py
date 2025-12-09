from django.contrib import admin
from .models import Notice

# Register your models here.
#admin.site.register(Notice)

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'posted_by', 'approved', 'is_active', 'expiry_date', 'created_at')
    list_filter = ('category', 'approved', 'is_active')
    search_fields = ('title', 'content')
    actions = ['approve_notices', 'deactivate_notices']