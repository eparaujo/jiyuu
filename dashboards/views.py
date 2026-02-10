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
from dojos.models import DojoMembership



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
        user = request.user

        # 🔹 Descobre vínculo do usuário com o dojo
        membership = (
            DojoMembership.objects
            .select_related("dojo")
            .filter(user=user)
            .first()
        )

        if not membership:
            return Response(
                {"detail": "Usuário sem vínculo com dojo"},
                status=status.HTTP_403_FORBIDDEN,
            )

        dojo = membership.dojo
        role = membership.role

        # 🔹 Seleciona dashboard conforme papel
        if role in ["OWNER", "ADMIN"]:
            dashboard = (
                Dashboard.objects
                .select_related("dojo")
                .filter(dojo=dojo)
                .first()
            )
        else:
            # STUDENT (ou qualquer outro papel)
            dashboard = (
                Dashboard.objects
                .select_related("dojo")
                .filter(dojo=dojo)
                .first()
            )

        if not dashboard:
            return Response(
                {"detail": "Dashboard não encontrado"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DashboardSerializer(
            dashboard,
            context={"request": request}
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
        

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
