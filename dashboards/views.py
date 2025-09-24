from typing import Any
from django.db.models.query import QuerySet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms
from dashboards.serializers import DashboardSerializer
from dashboards.models import Dashboard
from django.http import HttpResponse



class DashboardListView(LoginRequiredMixin, ListView):
    model = models.Dashboard
    template_name = "dashboard_list.html"
    context_object_name = "dashboards"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        dojo_name = self.request.GET.get("dojo")
        
        if dojo_name:
            queryset = queryset.filter(dojo__name__icontains=dojo_name)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context

class DashboardAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        try:
            dashboard = Dashboard.objects.first()  # ou filtrar pelo usuário, dojo etc.
            serializer = DashboardSerializer(dashboard)
            return Response(serializer.data)
        except Dashboard.DoesNotExist:
            return Response({"detail": "Nenhum dashboard encontrado"}, status=404)

class DashboardCreateView(LoginRequiredMixin, CreateView):
    model = models.Dashboard
    template_name = "dashboard_create.html"
    form_class = forms.DashboardForm
    success_url = reverse_lazy("dashboard_list")


class DashboardDetailView(LoginRequiredMixin, DetailView):
    model = models.Dashboard
    template_name = "dashboard_detail.html"
    context_object_name = "dashboard"


class DashboardUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Dashboard
    template_name = "dashboard_update.html"
    form_class = forms.DashboardForm
    success_url = reverse_lazy("dashboard_list")


class DashboardDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Dashboard
    template_name = "dashboard_delete.html"
    success_url = reverse_lazy("dashboard_list")