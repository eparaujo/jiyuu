from django import forms
from . import models


class InflowForm(forms.ModelForm):

    class Meta:
        model = models.Inflow
        fields = ['revenue', 'value', 'description']
        widgets = {
            'revenue': forms.Select(attrs={'class': 'form-control'}),            
            'value':  forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'revenue': 'Tipo de Receita',            
            'value':'Valor da Entrada',
            'description': 'Descrição',
        } 