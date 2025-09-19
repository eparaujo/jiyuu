from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models, forms
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class SenseiListView(LoginRequiredMixin, ListView):
    model = models.Sensei
    template_name = 'sensei_list.html'
    context_object_name ='senseis'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class SenseiCreateView(LoginRequiredMixin, CreateView):
    model = models.Sensei
    template_name = 'sensei_create.html'
    form_class = forms.SenseiForm
    success_url = reverse_lazy('sensei_list')

class SenseiDetailView(LoginRequiredMixin, DeleteView):
    model = models.Sensei
    template_name = 'sensei_detail.html'

class SenseiUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Sensei
    template_name = 'sensei_update.html'
    form_class = forms.SenseiForm
    success_url = reverse_lazy('sensei_list')

class SenseiDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Sensei
    template_name = 'sensei_delete.html'
    success_url = reverse_lazy('sensei_list')