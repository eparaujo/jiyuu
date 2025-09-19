from django.contrib import admin
from . import models

class OutflowAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'description')
    search_fields = ('name',)

admin.site.register(models.Outflow, OutflowAdmin) 