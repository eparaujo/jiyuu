from django.contrib import admin
from . import models


class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('karateca', 'event', 'enrolled_at',)
    search_fields = ('event',)

admin.site.register (models.CourseEnrollment, CourseEnrollmentAdmin)