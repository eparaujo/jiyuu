from django.contrib import admin
from . import models

class KaratecaAdmin(admin.ModelAdmin):
    list_display = ('name', 'genre', 'cpf', 'email', 'celphone', 'graduation', 'dojo', 'monthlypay', 'active', 'total_karatecas',)
    search_fields = ('name',)

admin.site.register(models.Karateca, KaratecaAdmin)