from django import forms
from . import models


class SenseiForm(forms.ModelForm):

    class Meta:
        model = models.Sensei
        fields = ['name', 'cpf', 'graduation', 'email', 'celPhone']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'graduation': forms.Select(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'celPhone':forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nome',
            'cpf': 'Número do CPF',
            'graduation': 'Graduação',
            'email': 'Endereço de E-mail',
            'celPhone': 'Número do Telefone Celuar-Whatsapp',
        }