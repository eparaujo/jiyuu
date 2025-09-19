from django import forms
from . import models
 

class DojoForm(forms.ModelForm):

    class Meta:
        model = models.Dojo
        fields = ['razaosocial', 'tradename', 'site', 'email', 'whatsapp', 'phone', 'street', 'number', 'zipcode', 'district', 'city',
                  'state', 'country', 'aulas',  'sensei']
        widgets = {
            'razaosocial': forms.TextInput(attrs={'class': 'form-control'}),
            'tradename': forms.TextInput(attrs={'class': 'form-control'}),
            'site': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'number': forms.NumberInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'aulas': forms.SelectMultiple(),
            'sensei': forms.SelectMultiple(),

        }
        labels = {
            'razaosocial': 'Razão Social',
            'tradename': 'Nome do Dojo',
            'site': 'Edereço do Site',
            'email': 'E-mail do Dojo',
            'whatsapp': 'Número do Whatsapp',
            'phone': 'Telefone Fixo',
            'street': 'Rua-Av.-Trav',
            'number': 'Número',
            'zipcode': 'CEP',
            'district': 'Bairro',
            'city': 'Cidade',
            'state': 'UF',
            'country': 'País',
            'aulas': 'Aulas - Treino',
            'sensei': 'Senseis',
        }

