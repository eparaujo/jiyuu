from django import forms
from . import models


class OutflowForm(forms.ModelForm):

    class Meta:
        model = models.Outflow
        fields = ['name', 'expense', 'value', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'expense': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'name': 'Saída - Nome',
            'expense': 'Tipo de Despesa',
            'value': 'Valor',
            'description': 'Descrição',
        }