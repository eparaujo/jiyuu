from django import forms
from . import models


from django import forms
from . import models
from graduations.models import Graduation


class EventForm(forms.ModelForm):

    class Meta:
        model = models.Event

        fields = [
            'name',
            'kind',
            'level',
            'date',
            'start_time',
            'end_time',
            'local',
            'address',
            'description',
            'hability_graduation',
            'category',
            'modality',
            'registration_fee',
            'limite_date',
            'organizer',
            'event_organizer',
            'status'
        ]

        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'kind': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'level': forms.Select(
                attrs={'class': 'form-control'}
            ),

            'date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'start_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),

            'end_time': forms.TimeInput(
                attrs={
                    'type': 'time',
                    'class': 'form-control'
                }
            ),

            'local': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'address': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'description': forms.Textarea(
                attrs={'class': 'form-control'}
            ),

            'hability_graduation': forms.CheckboxSelectMultiple(),

            'category': forms.CheckboxSelectMultiple(),

            'modality': forms.CheckboxSelectMultiple(),

            'registration_fee': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'step': '0.01',
                    'placeholder': '0.00'
                }
            ),

            'limite_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'organizer': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'event_organizer': forms.TextInput(
                attrs={'class': 'form-control'}
            ),

            'status': forms.Select(
                attrs={'class': 'form-control'}
            ),
        }

        labels = {
            'name': 'Evento',
            'kind': 'Tipo',
            'level': 'Nível',
            'date': 'Data do Evento',
            'start_time': 'Hora do Início',
            'end_time': 'Hora de Fim',
            'local': 'Local do Evento',
            'address': 'Endereço (Rua)',
            'description': 'Descrição',
            'hability_graduation': 'Graduações Habilitadas',
            'category': 'Categoria',
            'modality': 'Modalidade',
            'registration_fee': 'Valor da Inscrição - R$',
            'limite_date': 'Data Limite p/ Inscrição',
            'organizer': 'Entidade Organizadora',
            'event_organizer': 'Responsável pelo Evento',
            'status': 'Status'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['hability_graduation'].queryset = (
            Graduation.objects.all().order_by('order')
        )

        self.fields['category'].queryset = (
            models.Category.objects.all().order_by('name')
        )

        self.fields['modality'].queryset = (
            models.Modality.objects.all().order_by('name')
        )
