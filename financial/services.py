from datetime import datetime
from django.db.models import Sum
from invoices.models import Invoice
from inflows.models import Inflow
from outflows.models import Outflow
from events.models import Event

def get_financial_metrics(month=None, year=None):

    today = datetime.now()
    month = month or today.month
    year = year or today.year

    # 🔹 INVOICES (mensalidades)
    invoices = Invoice.objects.filter(
        billing_cycle__month=month,
        billing_cycle__year=year
    )

    paid_invoices = invoices.filter(paid=True)
    open_invoices = invoices.filter(paid=False)

    total_monthly_paid = paid_invoices.aggregate(total=Sum('total_amount'))['total'] or 0
    total_monthly_open = open_invoices.aggregate(total=Sum('total_amount'))['total'] or 0

    # 🔹 INFLOWS (entrada extra)
    inflows = Inflow.objects.filter(
        created_at__month=month,
        created_at__year=year
    )

    total_inflow = inflows.aggregate(total=Sum('value'))['total'] or 0

    # 🔹 EVENTOS
    events = Event.objects.filter(
        date__month=month,
        date__year=year
    )

    total_events = 0
    for event in events:
        total_enrolled = event.courseenrollment_set.count()
        total_events += event.registration_fee * total_enrolled

    # 🔹 OUTFLOWS (despesas)
    outflows = Outflow.objects.filter(
        created_at__month=month,
        created_at__year=year
    )

    total_expense = outflows.aggregate(total=Sum('value'))['total'] or 0

    # 🔥 CAIXA REAL
    total_revenue = total_monthly_paid + total_inflow + total_events
    total_profit = total_revenue - total_expense

    return {
        "revenue": float(total_revenue),
        "expenses": float(total_expense),
        "profit": float(total_profit),

        "breakdown": {
            "mensalidades": float(total_monthly_paid),
            "eventos": float(total_events),
            "outros": float(total_inflow),
        },

        # 🔥 NOVO
        "forecast": {
            "to_receive": float(total_monthly_open),
            "expected_total": float(total_revenue + total_monthly_open)
        }
    }

