from django.contrib import admin
from . import models

class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'day', 'start', 'end', 'sensei', 'description',)
    search_fields = ('name',)

admin.site.register(models.Aula, ClassAdmin)

