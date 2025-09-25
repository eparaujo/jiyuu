# exams/forms.py
from django import forms
from . import models


# -------------------------------
# EXAM
# -------------------------------
class ExamForm(forms.ModelForm):
    class Meta:
        model = models.Exam
        fields = ["dojo", "date", "description"]
        widgets = {
            "dojo": forms.Select(attrs={"class": "form-control"}),
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        labels = {
            "dojo": "Dojo",
            "date": "Data do Exame",
            "description": "Descrição / Observações",
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
        fields = ["exam", "subject", "max_score", "min_score"]
        widgets = {
            "exam": forms.Select(attrs={"class": "form-control"}),
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
        model = models.ExamEnrollment
        fields = ["exam", "karateca", "current_graduation"]
        widgets = {
            "exam": forms.Select(attrs={"class": "form-control"}),
            "karateca": forms.Select(attrs={"class": "form-control"}),
            "current_graduation": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "exam": "Exame",
            "karateca": "Karateca",
            "current_graduation": "Graduação Atual",
        }


# -------------------------------
# EXAM RESULT
# -------------------------------
class ExamResultForm(forms.ModelForm):
    class Meta:
        model = models.ExamResult
        fields = ["enrollment", "subject", "score", "comments"]
        widgets = {
            "enrollment": forms.Select(attrs={"class": "form-control"}),
            "subject": forms.Select(attrs={"class": "form-control"}),
            "score": forms.NumberInput(attrs={"class": "form-control"}),
            "comments": forms.Textarea(attrs={"class": "form-control"}),
        }
        labels = {
            "enrollment": "Inscrição (Aluno no Exame)",
            "subject": "Matéria",
            "score": "Nota",
            "comments": "Comentários",
        }
