from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models, forms
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


class KarateStyleListView(LoginRequiredMixin, ListView):
    model = models.KarateStyle
    template_name = 'karatestyle_list.html'
    context_object_name ='karatestyles'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        originstyle = self.request.GET.get('originstyle')
        bases = self.request.GET.get('bases')
        qtdekatas = self.request.GET.get('qtdekatas')
        

        if name:
            queryset = queryset.filter(name__icontains=name) #ignora case sensitive, semelhante a like no sql

        return queryset
    
    
class KarateStyleCreateView(LoginRequiredMixin, CreateView):
    model = models.KarateStyle
    template_name = 'karatestyle_create.html'
    form_class = forms.KarateStyleForm
    success_url = reverse_lazy('karatestyle_list')

class KarateStyleDetailView(LoginRequiredMixin, DeleteView):
    model = models.KarateStyle
    template_name = 'karatestyle_detail.html'

class KarateStyleUpdateView(LoginRequiredMixin, UpdateView):
    model = models.KarateStyle
    template_name = 'karatestyle_update.html'
    form_class = forms.KarateStyleForm
    success_url = reverse_lazy('karatestyle_list')

class KarateStyleDeleteView(LoginRequiredMixin, DeleteView):
    model = models.KarateStyle
    template_name = 'karatestyle_delete.html'
    success_url = reverse_lazy('karatestyle_list')