from django import forms
from . import models


class KaratecaForm(forms.ModelForm):

    class Meta:
        model = models.Karateca
        fields = ['name', 'genre', 'cpf', 'email', 'celphone', 'graduation', 'dan', 'dojo', 'active', 'monthly_fee', 'due_day']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'celphone':forms.TextInput(attrs={'class': 'form-control'}),
            'graduation': forms.Select(attrs={'class': 'form-control'}),
            'dan': forms.Select(attrs={'class': 'form-control'}),
            'dojo': forms.Select(attrs={'class': 'form-control'}),
            'active': forms.Select(attrs={'class': 'form-control'}),
            'monthly_fee': forms.TextInput(attrs={'placeholder': 'DD','class': 'form-control' }),
            'due_day': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
        }
        labels = {
            'name': 'Nome',
            'genre': 'Sexo',
            'cpf': 'Número do CPF',
            'email': 'Endereço de E-mail',
            'celPhone': 'Número do Telefone Celuar-Whatsapp',
            'graduation': 'Graduação',
            'dan': 'Definido quando se tratar de Faixa Preta',
            'dojo': 'Dojo',
            'active': 'Status',
            'monthly_fee': 'Valor da Mensalidade',
            'due_day': 'Data de Vencimento',
        }


class SetPasswordForm(forms.Form):
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm_password")

        if password != confirm:
            raise forms.ValidationError("As senhas não coincidem.")

        return cleaned_data