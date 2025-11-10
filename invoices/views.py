from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.core.management import call_command
from django.db.models import Sum
from .models import Invoice  
from karatecas.models import Karateca
from billingCycle.models import BillingCycle
from datetime import date
from decimal import Decimal
from django.utils import timezone
import calendar


# === ListView de faturas ===
class InvoiceListView(LoginRequiredMixin, ListView):
    model = Invoice
    template_name = 'invoice_list.html'   
    context_object_name = 'invoices'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset().select_related('karateca', 'billing_cycle').prefetch_related('items')
        # Substitua order_by('-issue_date') -> usar created_at ou billing_cycle
        qs = qs.order_by('-created_at')   # <-- CORREÇÃO principal
        # filtros opcionais
        karateca_q = self.request.GET.get('karateca')
        status = self.request.GET.get('status')  # ex: 'paid' ou 'pending'
        if karateca_q:
            qs = qs.filter(karateca__name__icontains=karateca_q)
        if status == 'paid':
            qs = qs.filter(paid=True)
        elif status == 'pending':
            qs = qs.filter(paid=False)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        totals = Invoice.objects.aggregate(total_all=Sum('total_amount'))
        ctx['total_amount'] = totals.get('total_all') or 0
        return ctx


# === DetailView para ver itens da invoice ===
class InvoiceDetailView(LoginRequiredMixin, DetailView):
    model = Invoice
    template_name = 'invoice_detail.html'
    context_object_name = 'invoice'

    def get_queryset(self):
        return super().get_queryset().select_related('karateca', 'billing_cycle').prefetch_related('items')


# === View para gerar faturas via botão ===
@login_required
def invoice_list_view(request):
    invoices = Invoice.objects.select_related("karateca", "billing_cycle").order_by("-due_date")

    # ciclo atual
    today = date.today()
    billing_cycle, _ = BillingCycle.objects.get_or_create(
        month=today.month,
        year=today.year,
        defaults={
            'start_date': date(today.year, today.month, 1),
            'end_date': date(today.year, today.month, calendar.monthrange(today.year, today.month)[1]),
        },
    )

    context = {
        "invoices": invoices,
        "billing_cycle": billing_cycle,
    }
    return render(request, "invoices/invoice_list.html", context)


@login_required
def generate_invoices_view(request):
    today = date.today()
    billing_cycle, _ = BillingCycle.objects.get_or_create(
        month=today.month,
        year=today.year,
        defaults={
            'start_date': date(today.year, today.month, 1),
            'end_date': date(today.year, today.month, calendar.monthrange(today.year, today.month)[1]),
        },
    )

    if billing_cycle.closed:
        messages.warning(request, '⚠️ Este ciclo de faturamento já está fechado.')
        return redirect('invoice_list')

    karatecas = Karateca.objects.filter(active="ATIVO")
    created_count = 0

    for k in karatecas:
        if k.monthly_fee and k.monthly_fee > 0:
            due_date = date(today.year, today.month, min(k.due_day, 28))
            exists = Invoice.objects.filter(karateca=k, billing_cycle=billing_cycle).exists()
            if not exists:
                Invoice.objects.create(
                    karateca=k,
                    billing_cycle=billing_cycle,
                    due_date=due_date,
                    total_amount=Decimal(k.monthly_fee),
                )
                created_count += 1

    if created_count > 0:
        messages.success(request, f'✅ {created_count} fatura(s) gerada(s) com sucesso!')
    else:
        messages.info(request, 'Nenhuma nova fatura gerada. Todas já existem para este mês.')

    return redirect('invoice_list')

@login_required
def close_cycle_view(request):
    today = date.today()
    cycle = BillingCycle.objects.filter(month=today.month, year=today.year).first()
    if not cycle:
        messages.error(request, "❌ Nenhum ciclo encontrado para este mês.")
        return redirect("invoice_list")

    cycle.close_cycle()
    messages.success(request, "🔒 Ciclo fechado com sucesso.")
    return redirect("invoice_list")


@login_required
def reset_cycle_view(request):
    today = date.today()
    cycle = BillingCycle.objects.filter(month=today.month, year=today.year).first()
    if not cycle:
        messages.error(request, "❌ Nenhum ciclo encontrado para este mês.")
        return redirect("invoice_list")

    deleted = cycle.reset_cycle(confirm=True)
    messages.success(request, f"♻️ {deleted} fatura(s) apagada(s) e ciclo reaberto.")
    return redirect("invoice_list")


# === View para marcar fatura como paga ===
@login_required
def mark_invoice_paid(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if not invoice.paid:
        invoice.paid = True
        invoice.paid_at = timezone.now() if hasattr(invoice, 'paid_at') else None
        invoice.save()
        messages.success(request, f'Fatura #{invoice.id} marcada como paga com sucesso!')
    else:
        messages.info(request, f'Fatura #{invoice.id} já estava marcada como paga.')
    return redirect('invoice_list')
