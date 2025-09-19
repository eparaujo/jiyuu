from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models, forms
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class KindRevenueListView(LoginRequiredMixin, ListView):
    model = models.KindRevenue
    template_name = 'kindrevenue_list.html'
    context_object_name ='kindrevenues'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class KindRevenueCreateView(LoginRequiredMixin, CreateView):
    model = models.KindRevenue
    template_name = 'kindrevenue_create.html'
    form_class = forms.KindRevenueForm
    success_url = reverse_lazy('kindrevenue_list')

class KindRevenueDetailView(LoginRequiredMixin, DeleteView):
    model = models.KindRevenue
    template_name = 'kindrevenue_detail.html'

class KindRevenueUpdateView(LoginRequiredMixin, UpdateView):
    model = models.KindRevenue
    template_name = 'kindrevenue_update.html'
    form_class = forms.KindRevenueForm
    success_url = reverse_lazy('kindrevenue_list')

class KindRevenueDeleteView(LoginRequiredMixin, DeleteView):
    model = models.KindRevenue
    template_name = 'kindrevenue_delete.html'
    success_url = reverse_lazy('kindrevenue_list')