from django.contrib import admin
from . import models

class PostureAdmin(admin.ModelAdmin):
    list_display = ('name', 'style', 'description', 'file')
    search_fields = ('name',)

admin.site.register(models.Posture, PostureAdmin)