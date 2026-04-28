from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from . import models, forms
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum
from revenues.models import Revenue
from django.db.models import Sum
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect


class RevenueListView(LoginRequiredMixin, ListView):
    model = models.Revenue
    template_name = 'revenue_list.html'
    context_object_name ='revenues'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.GET.get('name')
        
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    
class RevenueCreateView(LoginRequiredMixin, CreateView):
    model = models.Revenue
    template_name = 'revenue_create.html'
    form_class = forms.RevenueForm
    success_url = reverse_lazy('revenue_list')

class RevenueDetailView(LoginRequiredMixin, DeleteView):
    model = models.Revenue
    template_name = 'revenue_detail.html'

class RevenueUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Revenue
    template_name = 'revenue_update.html'
    form_class = forms.RevenueForm
    success_url = reverse_lazy('revenue_list')

class RevenueDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Revenue
    template_name = 'revenue_delete.html'
    success_url = reverse_lazy('revenue_list')

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as e:
            # Log para depuração (opcional)
            messages.error(request,
                "Não é possível excluir este registro, pois ele está sendo usado em outro lugar.")
            return redirect(self.success_url)
        

class FinancialDashboardAPIView(APIView):
    def get(self, request):
        now = datetime.now()
        """
        current_year = now.year
        current_month = str(now.month).zfill(2)

        # 🔹 RECEITAS
        revenues = Revenue.objects.filter(
            duedate__startswith=f"{current_year}-{current_month}"
        ).exclude(
            type__name__icontains="despesa"
        )

        # 🔹 DESPESAS
        expenses = Revenue.objects.filter(
            duedate__startswith=f"{current_year}-{current_month}",
            type__name__icontains="despesa"
        )"""

        revenues = Revenue.objects.exclude(
            type__name__icontains="despesa"
        )

        expenses = Revenue.objects.filter(
            type__name__icontains="despesa"
        )        

        total_revenue = revenues.aggregate(total=Sum('value'))['total'] or 0
        total_expenses = expenses.aggregate(total=Sum('value'))['total'] or 0

        return Response({
            "revenue": float(total_revenue),
            "expenses": float(total_expenses),
            "profit": float(total_revenue - total_expenses)
        })