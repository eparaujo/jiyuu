from django import forms
from .models import Graduation


class GraduationForm(forms.ModelForm):

    class Meta:
        model = Graduation
        fields = ['name', 'order', 'min_months']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'order': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
            'min_months': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1
            }),
        }

        labels = {
            'name': 'Graduação de Faixa',
            'order': 'Ordem da Graduação',
            'min_months': 'Carência mínima (meses)',
        }

        help_texts = {
            'order': 'Define a sequência das faixas (1 = iniciante)',
            'min_months': 'Tempo mínimo para poder realizar o próximo exame',
        }