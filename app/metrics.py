from karatecas.models import Karateca
from revenues.models import Revenue
from expenses.models import Expense
from inflows.models import Inflow
from invoices.models import Invoice
from events.models import Event
from outflows.models import Outflow
from django.utils.formats import number_format
from django.utils import timezone
from django.db.models import Sum, F


def get_karateca_metrics():
    revenues = Revenue.objects.all()
    expenses = Expense.objects.all()
    inflows  = Inflow.objects.all()
    outflows = Outflow.objects.all() 
     
    total_karatecas = 0
     
    total_karatecas = Karateca.objects.count()
    # Totais por status
    total_ativos = Karateca.objects.filter(active='ATIVO').count()
    total_afastados = Karateca.objects.filter(active='AFASTADO').count()
    total_licenciados = Karateca.objects.filter(active='LICENCIADO').count()
    total_cancelados = Karateca.objects.filter(active='CANCELADO').count()

    return dict(
        total_karatecas=total_karatecas,
        total_ativos=total_ativos,
        total_afastados=total_afastados,
        total_cancelados=total_cancelados,
        total_licenciados=total_licenciados
    )

def get_revenue_metrics():
    revenues = Revenue.objects.all()
    expenses = Expense.objects.all()
    inflows  = Inflow.objects.all()
    outflows = Outflow.objects.all()
    invoices = Invoice.objects.all()
    events   = Event.objects.all()
    

    # total de eventos = valor da inscrição * número de inscritos (CourseEnrollment)
    total_events = 0 
    for event in events:
        total_enrolled = event.courseenrollment_set.count()  # usa o related_name padrão
        total_events += event.registration_fee * total_enrolled

    #total_events = sum(event.registration_fee for event in events)
    total_revenue = sum(invoice.total_amount for invoice in invoices) + total_events
    total_monthly_fee = sum(invoice.total_amount for invoice in invoices)
    total_expense = sum(outflow.value for outflow in outflows)
    total_profit = total_revenue - total_expense
    

    return dict(
        total_revenue=number_format(total_revenue, decimal_pos=2, force_grouping=True),
        total_expense=number_format(total_expense, decimal_pos=2, force_grouping=True),
        total_profit=number_format(total_profit, decimal_pos=2, force_grouping=True),
        total_events=number_format(total_events, decimal_pos=2, force_grouping=True),
        total_monthly_fee=number_format(total_monthly_fee, decimal_pos=2, force_grouping=True),
        )

def get_expense_data(): #esta função é usada para calcular e passar os dados no contexto da view, a ser utilizada no gráfico da home
    today = timezone.now().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(30, -1, -1)] #aqui se cria uma lista com dados dos últimos 7 dias
    values = list()

    for date in dates:
        expense_total = Outflow.objects.filter(
            created_at__date=date
        ).aggregate(
            total_expenses = Sum(F('expense__value')*1)
        )['total_expenses'] or 0
        values.append(float(expense_total))

    return dict(
        dates=dates,
        values=values,
    )

def get_revenues_data():
    today = timezone.now().date()
    dates = [str(today - timezone.timedelta(days=i)) for i in range(30, -1, -1)] #aqui se cria uma lista com dados dos últimos 7 dias
    values = list()

    for date in dates:
        revenue_total = Inflow.objects.filter(
            created_at__date=date
        ).aggregate(
            total_revenue=Sum(F('revenue__value')*1)
        )['total_revenue'] or 0
        values.append(float(revenue_total))

    return dict(
        dates=dates,
        values=values,
    )