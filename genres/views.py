from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models, forms
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from . import serializers
from rest_framework import generics, permissions



class GenreListView(LoginRequiredMixin, ListView):
    model = models.Genre
    template_name = 'genre_list.html'
    context_object_name ='genres'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class GenreCreateView(LoginRequiredMixin, CreateView):
    model = models.Genre
    template_name = 'genre_create.html'
    form_class = forms.GenreForm
    success_url = reverse_lazy('genre_list')

class GenreDetailView(LoginRequiredMixin, DeleteView):
    model = models.Genre
    template_name = 'genre_detail.html'

class GenreUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Genre
    template_name = 'genre_update.html'
    form_class = forms.GenreForm
    success_url = reverse_lazy('genre_list')

class GenreDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Genre
    template_name = 'genre_delete.html'
    success_url = reverse_lazy('genre_list')

# 🔹 Lista todos os gêneros
class GenreListAPI(generics.ListAPIView):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    ermission_classes = [permissions.AllowAny]  # ✅ Permite acesso público