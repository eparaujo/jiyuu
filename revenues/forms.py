from django import forms
from . import models


class RevenueForm(forms.ModelForm):

    class Meta:
        model = models.Revenue
        fields = ['name',  'type', 'duedate',]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            #'value':  forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
            'duedate': forms.TextInput(attrs={'placeholder': 'DD-MM','class': 'form-control' }),
        }
        labels = {
            'name': 'Nome',
            'type': 'Categoria da Receita',
            #'value': 'Valor',
            'duedate': 'Data de Vencimento',
        }