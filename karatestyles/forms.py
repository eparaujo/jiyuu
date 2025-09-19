from django import forms
from . import models


class KarateStyleForm(forms.ModelForm):

    class Meta:
        model = models.KarateStyle
        fields = ['name', 'originstyle', 'bases', 'qtdekatas']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'originstyle': forms.TextInput(attrs={'class': 'form-control'}),
            'bases': forms.TextInput(attrs={'class': 'form-control'}),
            'qtdekatas': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Estilo de Karatê',
            'originstyle': 'Origem do Karatê (ex. Okinawa, etc.)',
            'bases': 'Bases (baixa, normal, alta, etc.)',
            'qtdekatas': 'Número de Katas do Estilo',

        }