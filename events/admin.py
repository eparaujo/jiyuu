from django.contrib import admin
from .models import Event, CourseEnrollment, Category, Modality


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "name", "kind", "level", "date", "local",
        "registration_fee", "limite_date", "status"
    )
    search_fields = ("name",)
    filter_horizontal = ("hability_graduation", "category", "modality")


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("event", "karateca", "enrollment_date", "paid")
    list_filter = ("paid", "event")
    search_fields = ("karateca__name", "event__name")


admin.site.register(Category)
admin.site.register(Modality)
