from django.contrib import admin
from .models import Exam, ExamSubject, ExamRequirement, ExamEnrollment, ExamResult


# ============================
# Admin para o modelo Exam
# ============================
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ("dojo", "date", "status", "get_categories")
    list_filter = ("dojo", "date", "status", "categories")
    search_fields = ("dojo__tradename", "description", "status")

    def get_categories(self, obj):
        """Exibe as categorias associadas ao exame"""
        return ", ".join([c.name_category for c in obj.categories.all()])
    get_categories.short_description = "Categorias"


# ============================
# Admin para o modelo ExamSubject
# ============================
@admin.register(ExamSubject)
class ExamSubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


# ============================
# Admin para o modelo ExamRequirement
# ============================
@admin.register(ExamRequirement)
class ExamRequirementAdmin(admin.ModelAdmin):
    list_display = ("exam", "subject", "max_score", "min_score")
    list_filter = ("exam", "subject")


# ============================
# Admin para o modelo ExamEnrollment
# ============================
@admin.register(ExamEnrollment)
class ExamEnrollmentAdmin(admin.ModelAdmin):
    list_display = ("exam", "karateca", "current_graduation", "category", "approved")
    list_filter = ("exam", "current_graduation", "category")
    search_fields = ("karateca__name",)


# ============================
# Admin para o modelo ExamResult
# ============================
@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "subject", "score", "sensei_examiner")
    list_filter = ("subject", "score", "sensei_examiner")
    search_fields = ("enrollment__karateca__name", "sensei_examiner")
