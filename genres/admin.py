from django.contrib import admin
from . import models

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

admin.site.register(models.Genre, GenreAdmin)

