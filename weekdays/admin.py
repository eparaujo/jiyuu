from django.contrib import admin
from . import models

class WeekdayAdmin(admin.ModelAdmin):
    list_display = ('dayname',)
    search_fields = ('dayname',)

admin.site.register(models.Weekday, WeekdayAdmin)

