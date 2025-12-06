from django.contrib import admin
from .models import Event, EventRegistration


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'venue', 'date', 'time', 'organizer')
    search_fields = ('title', 'venue', 'organizer')
    list_filter = ('date',)
    actions = ['delete_selected']

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('event', 'student', 'attended', 'registered_at')
    list_filter = ('attended',)
    search_fields = ('event__title', 'student__username')