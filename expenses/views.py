from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models, forms
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class ExpenseListView(LoginRequiredMixin, ListView):
    model = models.Expense
    template_name = 'expense_list.html'
    context_object_name ='expenses'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = models.Expense
    template_name = 'expense_create.html'
    form_class = forms.ExpenseForm
    success_url = reverse_lazy('expense_list')

class ExpenseDetailView(LoginRequiredMixin, DeleteView):
    model = models.Expense
    template_name = 'expense_detail.html'

class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Expense
    template_name = 'expense_update.html'
    form_class = forms.ExpenseForm
    success_url = reverse_lazy('expense_list')

class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Expense
    template_name = 'expense_delete.html'
    success_url = reverse_lazy('expense_list')
