from django.contrib import admin
from . import models

class KarateStyleAdmin(admin.ModelAdmin):
    list_display = ('name', 'originstyle', 'bases', 'qtdekatas')
    search_fields = ('name',)

admin.site.register(models.KarateStyle, KarateStyleAdmin)
