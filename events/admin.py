from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'venue', 'date', 'time', 'organizer')
    search_fields = ('title', 'venue', 'organizer')
