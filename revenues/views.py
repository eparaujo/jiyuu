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
from app.metrics import get_revenue_metrics



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

        metrics = get_revenue_metrics()

        # 🔥 converter string formatada → float
        def parse_money(value):
            if not value:
                return 0.0
            return float(value.replace('.', '').replace(',', '.'))

        return Response({
            "revenue": parse_money(metrics["total_revenue"]),
            "expenses": parse_money(metrics["total_expense"]),
            "profit": parse_money(metrics["total_profit"]),

            "breakdown": {
                "mensalidades": parse_money(metrics["total_monthly_fee"]),
                "eventos": parse_money(metrics["total_events"]),
                "outros": 0.0  # 🔥 ainda não existe no metrics
            }
        })