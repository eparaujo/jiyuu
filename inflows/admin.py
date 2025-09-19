from django.contrib import admin
from . import models

class InflowAdmin(admin.ModelAdmin):
    list_display = ('value','description',) #'total_revenue'
    search_fields = ('name',)

admin.site.register(models.Inflow, InflowAdmin)