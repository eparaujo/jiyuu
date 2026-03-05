from django import forms
from . import models
from .models import ExamEnrollment
from examcategories.models import ExamCategory
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta

# -------------------------------
# EXAM
# -------------------------------
class ExamForm(forms.ModelForm):
    class Meta:
        model = models.Exam
        fields = ["dojo", "date", "description", "status", "categories"]
        widgets = {
            "dojo": forms.Select(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "status": forms.Select(attrs={"class": "form-control"}),
            "categories": forms.SelectMultiple(attrs={"class": "form-control"}),
        } 
        labels = {
            "dojo": "Dojo",
            "date": "Data do Exame",
            "description": "Descrição / Observações",
            "status": "Status do Exame",
            "categories": "Categorias do Exame",
        }
# -------------------------------
# EXAM SUBJECT
# -------------------------------
class ExamSubjectForm(forms.ModelForm):
    class Meta:
        model = models.ExamSubject
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
        }
        labels = {
            "name": "Nome da Matéria (ex: Kata, Kihon, Bunkai...)",
        }


# -------------------------------
# EXAM REQUIREMENT
# -------------------------------
class ExamRequirementForm(forms.ModelForm):
    class Meta:
        model = models.ExamRequirement
        fields = ["exam", "category","subject", "max_score", "min_score"]
        widgets = {
            "exam": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "subject": forms.Select(attrs={"class": "form-control"}),
            "max_score": forms.NumberInput(attrs={"class": "form-control"}),
            "min_score": forms.NumberInput(attrs={"class": "form-control"}),
        }
        labels = {
            "exam": "Exame",
            "subject": "Matéria",
            "max_score": "Nota Máxima",
            "min_score": "Nota Mínima para Aprovação",
        }

# -------------------------------
# EXAM ENROLLMENT
# -------------------------------
class ExamEnrollmentForm(forms.ModelForm):

    class Meta:
        model = ExamEnrollment
        fields = ["karateca", "current_graduation", "category"]

    def __init__(self, *args, **kwargs):
        exam = kwargs.pop("exam", None)
        if not exam:
            raise ValueError("ExamEnrollmentForm exige um exame")

        super().__init__(*args, **kwargs)

        self.exam = exam

        self.fields["karateca"].queryset = models.Karateca.objects.filter(
            dojo=exam.dojo,
            active="ATIVO"
        ).order_by("name")

        self.fields["category"].queryset = exam.categories.all()

# -------------------------------
# EXAM RESULT
# -------------------------------
class ExamResultForm(forms.ModelForm):
    class Meta:
        model = models.ExamResult
        fields = ["enrollment", "subject", "score", "comments", "sensei_examiner"]
        widgets = {
            "enrollment": forms.Select(attrs={"class": "form-control"}),
            "subject": forms.Select(attrs={"class": "form-control"}),
            "score": forms.NumberInput(attrs={"class": "form-control"}),
            "comments": forms.Textarea(attrs={"class": "form-control"}),
            "sensei_examiner": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "enrollment": "Inscrição (Aluno no Exame)",
            "subject": "Matéria",
            "score": "Nota",
            "comments": "Comentários",
            "sensei_examiner": "Sensei Examinador",
        }
