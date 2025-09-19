from django import forms
from . import models
import os


class KataForm(forms.ModelForm):

    class Meta:
        model = models.Kata
        fields = ['namekata', 'style', 'qtde_moviments', 'file', 'link']
        widgets = {
            'namekata': forms.TextInput(attrs={'class': 'form-control'}),
            'style':  forms.Select(attrs={'class': 'form-control'}),
            'qtde_moviments': forms.NumberInput(attrs={'min': 0, 'step': 1}),
            #'file': forms.FileField(label="Selecione um arquivo", required=False),
            #'link': forms.URLField(label="URL do site", required=True, help_text="Insira uma URL válida."),
        }
        labels = {
            'namekata': 'Nome do Kata',
            'style': 'Estilo do Karatê',
            'qtde_moviments': 'Quantidade de Movimentos do Kata',
            #'file': 'Vídeo do Kata',
            #'link': 'Link para vídeo do Kata',
        }
