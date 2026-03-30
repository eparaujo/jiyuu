from django import forms
from . import models
from .models import ExamEnrollment
from examcategories.models import ExamCategory
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta
from senseis.models import Sensei
from dojos.models import DojoMembership
from dojos.choices import DojoRole
from dojos.models import DojoMembership
from dojos.choices import DojoRole


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        dojo = None

        # 🔹 1. via instance (edição ou create via kwargs)
        enrollment = getattr(self.instance, "enrollment", None)

        # 🔹 2. via initial
        if not enrollment:
            enrollment_id = self.initial.get("enrollment")
            if enrollment_id:
                try:
                    enrollment = models.ExamEnrollment.objects.select_related("exam__dojo").get(id=enrollment_id)
                except models.ExamEnrollment.DoesNotExist:
                    pass

        # 🔹 3. via POST
        if not enrollment:
            enrollment_id = self.data.get("enrollment")
            if enrollment_id:
                try:
                    enrollment = models.ExamEnrollment.objects.select_related("exam__dojo").get(id=enrollment_id)
                except models.ExamEnrollment.DoesNotExist:
                    pass

        # 🔹 resolve dojo
        if enrollment:
            dojo = enrollment.exam.dojo

        # 🔹 monta lista de examinadores
        if dojo:
            examiners = DojoMembership.objects.filter(
                dojo=dojo,
                role=DojoRole.EXAMINER,
                is_active=True
            ).select_related("user")

            self.fields["sensei_examiner"] = forms.ChoiceField(
                choices=[
                    ("", "---------"),
                    *[
                        (
                            m.user.get_full_name() or m.user.username,
                            m.user.get_full_name() or m.user.username
                        )
                        for m in examiners
                    ]
                ],
                widget=forms.Select(attrs={"class": "form-control"}),
                required=False
            )
        else:
            self.fields["sensei_examiner"] = forms.ChoiceField(
                choices=[("", "---------")],
                widget=forms.Select(attrs={"class": "form-control"}),
                required=False
            )
