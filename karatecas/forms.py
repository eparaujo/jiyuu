from django import forms
from . import models


class KaratecaForm(forms.ModelForm):

    class Meta:
        model = models.Karateca
        fields = ['name', 'genre', 'cpf', 'email', 'celphone', 'graduation', 'dojo', 'monthlypay', 'active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'celphone':forms.TextInput(attrs={'class': 'form-control'}),
            'graduation': forms.Select(attrs={'class': 'form-control'}),
            'dojo': forms.Select(attrs={'class': 'form-control'}),
            'monthlypay': forms.Select(attrs={'class': 'form-control'}),
            'active': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Nome',
            'genre': 'Sexo',
            'cpf': 'Número do CPF',
            'email': 'Endereço de E-mail',
            'celPhone': 'Número do Telefone Celuar-Whatsapp',
            'graduation': 'Graduação',
            'dojo': 'Dojo',
            'monthlypay': 'Modalidade de Pagamento',
            'active': 'Status',
        }