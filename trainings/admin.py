from django.contrib import admin
from .models import TrainingAttendance


@admin.register(TrainingAttendance)
class TrainingAttendanceAdmin(admin.ModelAdmin):
    list_display = (
        "karateca",
        "dojo",
        "training_date",
        "present",
        "created_at",
    )
    list_filter = ("dojo", "present", "training_date")
    search_fields = ("karateca__name",)