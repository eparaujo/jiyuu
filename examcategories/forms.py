from django import forms
from . import models


class ExamCategoryForm(forms.ModelForm):

    class Meta:
        model = models.ExamCategory
        fields = ['name_category',  'description']
        
        widgets = {
            'name_category': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

        }
        labels = {
            'name_category': 'Categoria do Exame',
            'description': 'Descrição',
           
        } 