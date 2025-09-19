from django import forms
from . import models


class PostureForm(forms.ModelForm):

    class Meta:
        model = models.Posture
        fields = ['name', 'style', 'description', 'file']
        widgets = {
            'kata': forms.TextInput(attrs={'class': 'form-control'}),
            'style':  forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            #'file': forms.FileField(label="Selecione um arquivo", required=False),
            #'link': forms.URLField(label="URL do site", required=True, help_text="Insira uma URL válida."),
        }
        labels = {
            'name': 'Nome da Postura',
            'style': 'Estilo do Karatê',
            'description': 'Descrição',
            #'file': 'Vídeo do Postura',
            #'link': 'Link para vídeo do Kata',
        } 