from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models, forms
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from . import serializers
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from graduations.models import Graduation
from genres.models import Genre


class GraduationListView(LoginRequiredMixin, ListView):
    model = models.Graduation
    template_name = 'graduation_list.html'
    context_object_name ='graduations'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class GraduationCreateView(LoginRequiredMixin, CreateView):
    model = models.Graduation
    template_name = 'graduation_create.html'
    form_class = forms.GraduationForm
    success_url = reverse_lazy('graduation_list')

class GraduationDetailView(LoginRequiredMixin, DeleteView):
    model = models.Graduation
    template_name = 'graduation_detail.html'

class GraduationUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Graduation
    template_name = 'graduation_update.html'
    form_class = forms.GraduationForm
    success_url = reverse_lazy('graduation_list')

class GraduationDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Graduation
    template_name = 'graduation_delete.html'
    success_url = reverse_lazy('graduation_list')

 # 🔹 Lista todas as graduações
class GraduationListAPI(generics.ListAPIView):
    queryset = models.Graduation.objects.all()
    serializer_class = serializers.GraduationSerializer   
    ermission_classes = [permissions.AllowAny]  # ✅ Permite acesso público


class GraduationListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        graduations = Graduation.objects.all().order_by('order')

        data = [
            {
                "id": g.id,
                "name": g.name
            }
            for g in graduations
        ]

        return Response(data)
    
class GenreListAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        genres = Genre.objects.all()

        data = [
            {
                "id": g.id,
                "name": g.name 
            }
            for g in genres
        ]

        return Response(data)