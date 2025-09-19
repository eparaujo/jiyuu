from django.contrib import admin
from . import models

class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'level', 'date', 'start_time', 'end_time', 'local', 'adress', 'description', 'hability_graduation', 'category', 'modalitiy', 'registration_fee',
                    'limite_date', 'organizer', 'event_organizer', 'status',)
    
    search_fields = ('name',)

admin.site.register(models.Event, EventAdmin)