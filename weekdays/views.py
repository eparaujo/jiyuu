from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models, forms
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class WeekdaysListView(LoginRequiredMixin, ListView):
    model = models.Weekday
    template_name = 'weekdays_list.html'
    context_object_name ='weekdays'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        dayname = self.request.GET.get('dayname')
        
        if dayname:
            queryset = queryset.filter(dayname__icontains=dayname)
        return queryset
    
class WeekdaysCreateView(LoginRequiredMixin, CreateView):
    model = models.Weekday
    template_name = 'weekdays_create.html'
    form_class = forms.WeekdayForm
    success_url = reverse_lazy('weekdays_list')

class WeekdaysDetailView(LoginRequiredMixin, DeleteView):
    model = models.Weekday
    template_name = 'weekdays_detail.html'

class WeekdaysUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Weekday
    template_name = 'weekdays_update.html'
    form_class = forms.WeekdayForm
    success_url = reverse_lazy('weekdays_list')

class WeekdaysDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Weekday
    template_name = 'weekdays_delete.html'
    success_url = reverse_lazy('weekdays_list')