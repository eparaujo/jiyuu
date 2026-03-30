from django.contrib import admin
from . import models

class GraduationAdmin(admin.ModelAdmin):
    list_display = ('id','name',)
    search_fields = ('name',)

admin.site.register(models.Graduation, GraduationAdmin)