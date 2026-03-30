from django import forms
from . import models


class ExamCategoryForm(forms.ModelForm):

    class Meta:
        model = models.ExamCategory
        fields = ['name_category',  'description', 'to_graduation']
        
        widgets = {
            'name_category': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'to_graduation': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'name_category': 'Categoria do Exame',
            'description': 'Descrição',
            'to_graduation': 'Próxima Graduação',
        } 