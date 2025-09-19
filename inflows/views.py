from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models, forms
from django.views.generic import ListView, CreateView, DetailView 
from django.urls import reverse_lazy
from revenues.models import Revenue
from django.contrib.auth.mixins import LoginRequiredMixin


class InflowListView(LoginRequiredMixin, ListView):
    model = models.Inflow
    template_name = 'inflow_list.html'
    context_object_name ='inflows'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        revenue = self.request.GET.get('revenue')
        
        if revenue:
            queryset = queryset.filter(revenue_name__icontains=revenue) #estou filtrando pelo nome da revenue
        return queryset
    
class InflowCreateView(LoginRequiredMixin, CreateView):
    model = models.Inflow
    template_name = 'inflow_create.html'
    form_class = forms.InflowForm
    success_url = reverse_lazy('inflow_list')


class InflowDetailView(LoginRequiredMixin, DetailView):
    model = models.Inflow
    template_name = 'inflow_detail.html'