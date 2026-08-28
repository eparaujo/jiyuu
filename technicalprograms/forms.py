from django import forms
from . import models
from django.db.models import Q


class TechnicalProgramForm(forms.ModelForm):

    class Meta:
        model = models.TechnicalProgram

        fields = [
            "category",
            "style",
            "target",
            "description",
            "active",
        ]

        widgets = {
            "category": forms.Select(attrs={"class": "form-select",}),
            "style": forms.Select(attrs={"class": "form-select",}),
            "target": forms.TextInput(attrs={"class": "form-control",}),
            "description": forms.Textarea(attrs={"class": "form-control","rows": 3,}),
            "active": forms.CheckboxInput(attrs={"class": "form-check-input",}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        queryset = (
            models.ExamCategory.objects
            .select_related("to_graduation")
            .order_by(
                "to_graduation__order",
                "to_graduation__id",
            )
        )

        if self.instance.pk:
            queryset = queryset.filter(
                Q(technical_program__isnull=True)
                | Q(pk=self.instance.category_id)
            )

        self.fields["category"].queryset = queryset


class TechnicalProgramItemForm(forms.ModelForm):

    class Meta:
        model = models.TechnicalProgramItem

        fields = [
            "program",
            "modality",
            "title",
            "description",
            "sequence",
            "mandatory",
            "active",
        ]

        widgets = {
            "program": forms.Select(attrs={"class": "form-select",
                }
            ),
            "modality": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
            "sequence": forms.NumberInput(
                attrs={
                    "class": "form-control",
                }
            ),
            "mandatory": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
            "active": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["program"].queryset = (
            models.TechnicalProgram.objects
            .filter(active=True)
            .select_related(
                "category",
                "category__to_graduation",
            )
            .order_by(
                "category__to_graduation__order",
                "category__to_graduation__id",
            )
        )