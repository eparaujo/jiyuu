from django import forms
from . import models
from .models import ExamEnrollment
from examcategories.models import ExamCategory
from graduations.models import Graduation
from karatecas.models import Karateca
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta
from senseis.models import Sensei
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
            "date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={"class": "form-control", "type": "date"}
            ),
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
        fields = ["exam", "category","subject", "min_score", "max_score"]
        widgets = {
            "exam": forms.Select(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "subject": forms.Select(attrs={"class": "form-control"}),
            "min_score": forms.NumberInput(attrs={"class": "form-control"}),
            "max_score": forms.NumberInput(attrs={"class": "form-control"}),
        }
        labels = {
            "exam": "Exame",
            "subject": "Matéria",            
            "min_score": "Nota Mínima",
            "max_score": "Nota Máxima",
        }

# -------------------------------
# EXAM ENROLLMENT
# -------------------------------
class ExamEnrollmentForm(forms.ModelForm):

    # --------------------------------------------------
    # Campo apenas para visualização
    # --------------------------------------------------

    current_graduation_display = forms.CharField(
        label="Graduação atual",
        required=False,
        disabled=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    # --------------------------------------------------
    # Campo apenas para visualização
    # --------------------------------------------------

    next_graduation_display = forms.CharField(
        label="Próxima graduação",
        required=False,
        disabled=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control"
            }
        )
    )

    class Meta:
        model = models.ExamEnrollment

        # --------------------------------------------------
        # IMPORTANTE:
        #
        # current_graduation não entra aqui porque será
        # preenchido automaticamente pela View a partir
        # da graduação real do Karateca.
        #
        # current_graduation_display e
        # next_graduation_display são somente visuais.
        # --------------------------------------------------

        fields = [
            "karateca",
            "category",
        ]

        widgets = {
            "karateca": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
            "category": forms.Select(
                attrs={
                    "class": "form-control"
                }
            ),
        }

        labels = {
            "karateca": "Karateca",
            "category": "Categoria do Exame - Faixa",
        }

    def __init__(self, *args, exam=None, **kwargs):

        super().__init__(*args, **kwargs)

        self.exam = exam

        # --------------------------------------------------
        # 1. Inicialmente não temos karateca selecionado
        # --------------------------------------------------

        karateca = None

        # --------------------------------------------------
        # 2. Tenta descobrir o karateca selecionado
        #
        # Quando o formulário é carregado:
        #     self.data pode estar vazio.
        #
        # Quando o usuário seleciona um karateca:
        #     self.data["karateca"] terá o ID.
        # --------------------------------------------------

        karateca_id = (
            self.data.get("karateca")
            or self.initial.get("karateca")
        )

        if karateca_id:

            try:

                karateca = (
                    Karateca.objects
                    .select_related("graduation")
                    .get(pk=karateca_id)
                )

            except Karateca.DoesNotExist:

                karateca = None

        # --------------------------------------------------
        # 3. Mostra a graduação atual
        #
        # SOMENTE PARA VISUALIZAÇÃO.
        #
        # Não estamos atribuindo esse valor ao campo
        # current_graduation do Model.
        # --------------------------------------------------

        if karateca and karateca.graduation:

            self.fields[
                "current_graduation_display"
            ].initial = (
                karateca.graduation.name
            )

        else:

            self.fields[
                "current_graduation_display"
            ].initial = (
                "Sem graduação"
            )

        # --------------------------------------------------
        # 4. Descobre a próxima graduação
        # --------------------------------------------------

        next_graduation = None

        if karateca and karateca.graduation:

            next_graduation = (
                Graduation.objects
                .filter(
                    order__gt=karateca.graduation.order
                )
                .order_by("order")
                .first()
            )

        # --------------------------------------------------
        # 5. Mostra a próxima graduação
        #
        # SOMENTE PARA VISUALIZAÇÃO.
        # --------------------------------------------------

        if next_graduation:

            self.fields[
                "next_graduation_display"
            ].initial = (
                next_graduation.name
            )

        else:

            self.fields[
                "next_graduation_display"
            ].initial = (
                "Nenhuma graduação posterior"
            )

        # --------------------------------------------------
        # 6. Filtra as categorias do exame
        #
        # Somente categorias cuja graduação de destino
        # seja a próxima graduação do Karateca.
        # --------------------------------------------------

        if exam:

            categories = exam.categories.all()

            if next_graduation:

                categories = categories.filter(
                    to_graduation=next_graduation
                )

            self.fields["category"].queryset = categories

        # --------------------------------------------------
        # 7. Karatecas disponíveis
        #
        # Somente karatecas:
        # - do dojo do exame
        # - ativos
        # --------------------------------------------------

        if exam:

            self.fields[
                "karateca"
            ].queryset = (
                Karateca.objects
                .filter(
                    dojo=exam.dojo,
                    active="ATIVO"
                )
                .select_related("graduation")
                .order_by("name")
            )

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
