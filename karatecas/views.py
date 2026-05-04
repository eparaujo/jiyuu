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
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from .models import Karateca
from .forms import SetPasswordForm
from django.db.models import Count



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
    serializer_class = serializers.KaratecaSerializer

    def get_queryset(self):
        queryset = models.Karateca.objects.select_related(
                "graduation", "dojo", "genre").all()

        status = self.request.query_params.get("status")

        if status:
                queryset = queryset.filter(active__iexact=status.strip())

        return queryset.order_by("name")

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
    
#View para gravar senha
def set_karateca_password(request, pk):
    karateca = get_object_or_404(Karateca, pk=pk)

    if not karateca.user:
        messages.error(request, "Karateca não possui usuário vinculado.")
        return redirect("karateca_list")

    if request.method == "POST":
        form = SetPasswordForm(request.POST)

        if form.is_valid():
            password = form.cleaned_data["password"]

            user = karateca.user
            user.set_password(password)  # 🔐 CRÍTICO
            user.save()

            messages.success(request, "Senha definida com sucesso!")
            return redirect("karateca_list")
    else:
        form = SetPasswordForm()

    return render(request, "set_password.html", {
        "form": form,
        "karateca": karateca
    })

class StudentStatsAPIView(APIView):
    def get(self, request):
        stats = Karateca.objects.values('active').annotate(total=Count('id'))

        result = {
            "ATIVO": 0,
            "AFASTADO": 0,
            "LICENCIADO": 0,
            "CANCELADO": 0,
            "TOTAL": 0
        }

        for item in stats:
            status = item['active']
            total = item['total']
            result[status] = total
            result["TOTAL"] += total

        return Response(result)