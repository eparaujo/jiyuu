from django.contrib import admin
from . import models

class DojoAdmin(admin.ModelAdmin):
    list_display = ('razaosocial', 'tradename', 'site', 'email', 'whatsapp', 'phone', 'street', 'number', 'zipcode', 'district', 'city',
                  'state', 'country', )
    search_fields = ('tradename',)

admin.site.register(models.Dojo, DojoAdmin) 
