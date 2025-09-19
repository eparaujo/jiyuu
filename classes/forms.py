from django import forms
from . import models


class ClassForm(forms.ModelForm):

    class Meta:
        model = models.Aula
        fields = ['name', 'day', 'start', 'end', 'sensei', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'day': forms.Select(attrs={'class': 'form-control'}),
            'start': forms.TimeInput(format='%H:%M'),
            'end': forms.TimeInput(format='%H:%M'),
            'sensei': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

        }
        labels = {
            'name': 'Nome',
            'day': 'Dia da Semana',
            'start': 'Hora de Início',
            'end': 'Hora de Encerramento',
            'sensei': 'Sensei',
            'description': 'Descrição',
           
        } 