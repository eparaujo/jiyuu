from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models, forms
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class KataListView(LoginRequiredMixin, ListView):
    model = models.Kata
    template_name = 'kata_list.html'
    context_object_name ='katas'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        namekata = self.request.GET.get('namekata')
        
        if namekata:
            queryset = queryset.filter(namekata__icontains=namekata)
        return queryset
    
class KataCreateView(LoginRequiredMixin, CreateView):
    model = models.Kata
    template_name = 'kata_create.html'
    form_class = forms.KataForm
    success_url = reverse_lazy('kata_list')

class KataDetailView(LoginRequiredMixin, DeleteView):
    model = models.Kata
    template_name = 'kata_detail.html'

class KataUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Kata
    template_name = 'kata_update.html'
    form_class = forms.KataForm
    success_url = reverse_lazy('kata_list')

class KataDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Kata
    template_name = 'kata_delete.html'
    success_url = reverse_lazy('kata_list')
