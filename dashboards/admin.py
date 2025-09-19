from django.contrib import admin
from . import models

# Register your models here.

class DashboardAdmin(admin.ModelAdmin):
        list_display = ("dojo", "active_students", "last_exam_date", "last_exam_participants", "last_exam_approved", "last_exam_students", "next_exam_date", "next_exam_registered",
            "next_exam_students", "next_exam_name", "upcoming_events",)
        search_fields = ('name',)

admin.site.register(models.Dashboard, DashboardAdmin)