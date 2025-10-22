from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models, forms
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, permissions
from . import serializers


class KaratecaListView(LoginRequiredMixin, ListView):
    model = models.Karateca
    template_name = 'karateca_list.html'
    context_object_name ='karatecas'
    paginate_by = 15

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class KaratecaCreateView(LoginRequiredMixin, CreateView):
    model = models.Karateca
    template_name = 'karateca_create.html'
    form_class = forms.KaratecaForm
    success_url = reverse_lazy('karateca_list')

class KaratecaDetailView(LoginRequiredMixin, DeleteView):
    model = models.Karateca
    template_name = 'karateca_detail.html'

class KaratecaUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Karateca
    template_name = 'karateca_update.html'
    form_class = forms.KaratecaForm
    success_url = reverse_lazy('karateca_list')

class KaratecaDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Karateca 
    template_name = 'karateca_delete.html'
    success_url = reverse_lazy('karateca_list')

class KaratecaCreateListAPIView(generics.ListCreateAPIView):
    queryset = models.Karateca.objects.all()
    serializer_class = serializers.KaratecaSerializer

class KaratecaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Karateca.objects.all()
    serializer_class = serializers.KaratecaSerializer
    
class PublicKaratekaRegisterView(generics.CreateAPIView):
    queryset = models.Karateca.objects.all()
    serializer_class = serializers.PublicKaratekaRegisterSerializer
    permission_classes = [permissions.AllowAny]