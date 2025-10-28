from django.contrib import admin
from . import models

class KaratecaAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'genre', 'cpf', 'email', 'celphone', 'graduation', 'dan', 'dojo', 'active', 'monthly_fee', 'due_day',)
    search_fields = ('name',)

admin.site.register(models.Karateca, KaratecaAdmin)