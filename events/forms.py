from django import forms
from . import models


class EventForm(forms.ModelForm):
        
        class Meta:
            model = models.Event
            fields = ['name', 'kind', 'level', 'date', 'start_time', 'end_time', 'local', 'adress', 'description', 'hability_graduation', 'category', 'modalitiy', 'registration_fee',
                    'limite_date', 'organizer', 'event_organizer', 'status']
            
            widgets = {
                'name': forms.TextInput(attrs={'class': 'form-control'}), 
                'kind': forms.Select(attrs={'class': 'form-control'}), 
                'level': forms.Select(attrs={'class': 'form-control'}), 
                'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'DD-MM'}), 
                'start_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'HH:MM'}), 
                'end_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control', 'placeholder': 'HH:MM'}),  
                'local': forms.TextInput(attrs={'class': 'form-control'}),
                'adress': forms.TextInput(attrs={'class': 'form-control'}), 
                'description': forms.Textarea(attrs={'class': 'form-control'}), 
                'hability_graduation': forms.Select(attrs={'class': 'form-control'}),  
                'category': forms.Select(attrs={'class': 'form-control'}), 
                'modalitiy': forms.Select(attrs={'class': 'form-control'}),  
                'registration_fee': forms.NumberInput(attrs={'step': '0.01', 'placeholder': '0.00'}),
                'limite_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'DD-MM'}), 
                'organizer': forms.TextInput(attrs={'class': 'form-control'}), 
                'event_organizer': forms.TextInput(attrs={'class': 'form-control'}), 
                'status': forms.Select(attrs={'class': 'form-control'})
            }
            labels = {
                'name': 'Evento', 
                'kind': 'Tipo', 
                'level': 'Nível', 
                'date': 'Data do Evento', 
                'start_time': 'Hora do Início', 
                'end_time': 'Hora de Fim', 
                'local': 'Local do Evento', 
                'adress': 'Endereço (Rua)', 
                'description': 'Descrição', 
                'hability_graduation': 'Graduações Habilitadas', 
                'category': 'Categoria', 
                'modalitiy': 'Modalidade', 
                'registration_fee': 'Valor da Inscrição - R$',
                'limite_date':' Data Limite p/ Inscrição', 
                'organizer': 'Entidade Organizadora', 
                'event_organizer': 'Responsável pelo Evento', 
                'status': 'Status' 
            }
