from django import forms
from . import models


class KindRevenueForm(forms.ModelForm):

    class Meta:
        model = models.KindRevenue
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
        }
        labels = {
            'name': 'Tipo de Receita',
            'description': 'Descrição',
        } 