from django import forms
from . import models


class GraduationForm(forms.ModelForm):

    class Meta:
        model = models.Graduation
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Graduação de Faixa',
        }