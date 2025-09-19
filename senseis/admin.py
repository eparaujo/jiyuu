from django.contrib import admin
from . import models

class SenseiAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'graduation', 'email', 'celPhone',)
    search_fields = ('name',)

admin.site.register(models.Sensei, SenseiAdmin)