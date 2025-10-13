from django.contrib import admin
from .models import Exam, ExamSubject, ExamRequirement, ExamEnrollment, ExamResult

# ============================
# Admin para o modelo Exam
# ============================
@admin.register(Exam)  # Registra o modelo Exam no Django Admin
class ExamAdmin(admin.ModelAdmin):
    # Define quais campos serão exibidos na lista do Admin
    list_display = ("dojo", "date", "description", "status")
    # Permite filtrar a lista no Admin pelos campos definidos
    list_filter = ("dojo", "date")
    # Habilita a pesquisa por nome do dojo (tradename) e descrição
    search_fields = ("dojo__tradename", "description", "status")


# ============================
# Admin para o modelo ExamSubject
# ============================
@admin.register(ExamSubject)  # Registra o modelo ExamSubject
class ExamSubjectAdmin(admin.ModelAdmin):
    # Mostra apenas o nome da disciplina/prova na listagem
    list_display = ("name",)
    # Permite pesquisar pelo nome da disciplina/prova
    search_fields = ("name",)


# ============================
# Admin para o modelo ExamRequirement
# ============================
@admin.register(ExamRequirement)  # Registra o modelo ExamRequirement
class ExamRequirementAdmin(admin.ModelAdmin):
    # Exibe o exame, disciplina, nota máxima e mínima
    list_display = ("exam", "subject", "max_score", "min_score")
    # Permite filtrar por exame e disciplina
    list_filter = ("exam", "subject")


# ============================
# Admin para o modelo ExamEnrollment
# ============================
@admin.register(ExamEnrollment)  # Registra o modelo ExamEnrollment
class ExamEnrollmentAdmin(admin.ModelAdmin):
    # Exibe exame, karateca inscrito e graduação atual
    list_display = ("exam", "karateca", "current_graduation")
    # Permite filtrar por exame e graduação atual
    list_filter = ("exam", "current_graduation")
    # Permite pesquisar pelo nome do karateca (relacionamento)
    search_fields = ("karateca__name",)


# ============================
# Admin para o modelo ExamResult
# ============================
@admin.register(ExamResult)  # Registra o modelo ExamResult
class ExamResultAdmin(admin.ModelAdmin):
    # Exibe matrícula (inscrição), disciplina, nota e examinador
    list_display = ("enrollment", "subject", "score", "sensei_examiner")
    # Permite filtrar por disciplina, nota e examinador
    list_filter = ("subject", "score", "sensei_examiner")
    # Permite pesquisar pelo nome do karateca ou do examinador
    search_fields = ("enrollment__karateca__name", "sensei_examiner__name")
