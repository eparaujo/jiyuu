from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models, forms
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class ClassListView(LoginRequiredMixin, ListView):
    model = models.Aula
    template_name = 'class_list.html'
    context_object_name ='classes'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class ClassCreateView(LoginRequiredMixin, CreateView):
    model = models.Aula
    template_name = 'class_create.html'
    form_class = forms.ClassForm
    success_url = reverse_lazy('class_list')

class ClassDetailView(LoginRequiredMixin, DeleteView):
    model = models.Aula
    template_name = 'class_detail.html'

class ClassUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Aula
    template_name = 'class_update.html'
    form_class = forms.ClassForm
    success_url = reverse_lazy('class_list')

class ClassDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Aula
    template_name = 'class_delete.html'
    success_url = reverse_lazy('class_list')