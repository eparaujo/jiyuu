from django.contrib import admin
from . import models


class ExamCategoriesAdmin(admin.ModelAdmin):

    list_display = ('name_category', 'description','to_graduation',)
    search_fields = ('name_category',)

admin.site.register(models.ExamCategory, ExamCategoriesAdmin)