from django.contrib import admin
from . import models

class KataAdmin(admin.ModelAdmin):
    list_display = ('namekata', 'style', 'qtde_moviments', 'file', 'link',)
    search_fields = ('namekata',)

admin.site.register(models.Kata, KataAdmin)