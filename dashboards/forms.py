from django import forms
from . import models


class DashboardForm(forms.ModelForm):
    class Meta:
        model = models.Dashboard
        fields = ["dojo", "active_students", "last_exam_date", "last_exam_participants", "last_exam_approved", "last_exam_students", "next_exam_date", "next_exam_registered",
            "next_exam_students", "next_exam_name", "upcoming_events", 
            ]
        
        widgets = {
            "dojo": forms.Select(attrs={"class": "form-control"}),
            "active_students": forms.NumberInput(attrs={"class": "form-control"}),
            "last_exam_date": forms.DateInput(attrs={"type": "date", "class": "form-control", "placeholder": "DD-MM"}),
            "last_exam_participants": forms.NumberInput(attrs={"class": "form-control"}),
            "last_exam_approved": forms.NumberInput(attrs={"class": "form-control"}),
            "last_exam_students": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "next_exam_date": forms.DateInput(attrs={"type": "date", "class": "form-control", "placeholder": "DD-MM"}),
            "next_exam_registered": forms.NumberInput(attrs={"class": "form-control"}),
            "next_exam_students": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "next_exam_name": forms.TextInput(attrs={"class": "form-control"}),
            "upcoming_events": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
        labels = {
            "dojo": "Dojo",
            "active_students": "Alunos ativos",
            "last_exam_date": "Data do último exame",
            "last_exam_participants": "Participantes do último exame",
            "last_exam_approved": "Aprovados no último exame",
            "last_exam_students": "Alunos do último exame (JSON)",
            "next_exam_date": "Data do próximo exame",
            "next_exam_registered": "Inscritos no próximo exame",
            "next_exam_students": "Alunos do próximo exame (JSON)",
            "next_exam_name": "Nome do próximo exame",
            "upcoming_events": "Eventos futuros (JSON)",
        }
