from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models, forms
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, permissions
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import date
from graduations.models import Graduation
#from serializers import GraduationStatusSerializer


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


class KaratecaGraduationStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        karateca = request.user.karateka

        # Segurança
        if not karateca or not karateca.graduation:
            return Response({
                "current_graduation": None,
                "next_graduation": None,
                "min_months": 0,
                "elapsed_months": 0,
                "remaining_months": 0
            })

        current = karateca.graduation

        next_graduation = Graduation.objects.filter(
            order__gt=current.order
        ).order_by('order').first()

        if not next_graduation or not karateca.graduation_date:
            return Response({
                "current_graduation": current.name,
                "next_graduation": next_graduation.name if next_graduation else None,
                "min_months": next_graduation.min_months if next_graduation else 0,
                "elapsed_months": 0,
                "remaining_months": next_graduation.min_months if next_graduation else 0
            })

        # 🔹 cálculo de meses
        today = date.today()
        delta_months = (
            (today.year - karateca.graduation_date.year) * 12 +
            (today.month - karateca.graduation_date.month)
        )

        remaining = max(0, next_graduation.min_months - delta_months)

        data = {
            "current_graduation": current.name,
            "next_graduation": next_graduation.name,
            "min_months": next_graduation.min_months,
            "elapsed_months": delta_months,
            "remaining_months": remaining
        }

        serializer = GraduationStatusSerializer(data)
        return Response(serializer.data)