from django import forms
from . import models


class WeekdayForm(forms.ModelForm):

    class Meta:
        model = models.Weekday
        fields = ['dayname']
        widgets = {
            'dayname': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'dayname': 'Dia da Semana',
        }