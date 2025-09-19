from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models, forms
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class DojoListView(LoginRequiredMixin, ListView):
    model = models.Dojo
    template_name = 'dojo_list.html'
    context_object_name ='dojos'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        tradename = self.request.GET.get('tradename')
        
        if tradename:
            queryset = queryset.filter(tradename__icontains=tradename)
        return queryset
    
class DojoCreateView(LoginRequiredMixin, CreateView):
    model = models.Dojo
    template_name = 'dojo_create.html'
    form_class = forms.DojoForm
    success_url = reverse_lazy('dojo_list')

class DojoDetailView(LoginRequiredMixin, DeleteView):
    model = models.Dojo
    template_name = 'dojo_detail.html'

class DojoUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Dojo
    template_name = 'dojo_update.html'
    form_class = forms.DojoForm
    success_url = reverse_lazy('dojo_list')

class DojoDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Dojo
    template_name = 'dojo_delete.html'
    success_url = reverse_lazy('dojo_list')
