from django import forms
from . import models


class GenreForm(forms.ModelForm):

    class Meta:
        model = models.Genre
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name': 'Gênero',
        }