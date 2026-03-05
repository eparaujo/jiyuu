from django import forms
from dojos.models import Dojo
from karatecas.models import Karateca
from .models import TrainingAttendance
from django.utils import timezone


class AttendanceForm(forms.Form):
    dojo = forms.ModelChoiceField(
        queryset=Dojo.objects.all(),
        label="Dojo"
    )

    training_date = forms.DateField(
        label="Data do Treino",
        widget=forms.DateInput(attrs={"type": "date"}),
        initial=timezone.now
    )