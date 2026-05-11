from rest_framework.views import APIView
from rest_framework.response import Response
from .services import get_financial_metrics
from invoices.models import Invoice
from outflows.models import Outflow
from inflows.models import Inflow
from events.models import Event
from django.db.models import Sum
from django.db.models.functions import ExtractDay
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
from .serializers import FinancialDetailSerializer
from calendar import monthrange
from events.models import CourseEnrollment
from datetime import date


class FinancialDashboardAPIView(APIView):
    def get(self, request):
        month = request.GET.get("month")
        year = request.GET.get("year")

        data = get_financial_metrics(
            month=int(month) if month else None,
            year=int(year) if year else None
        )

        return Response(data)
    

from collections import defaultdict
from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response

class FinancialTimeseriesAPIView(APIView):

    def get(self, request):
        month = int(request.GET.get("month"))
        year = int(request.GET.get("year"))

        days = defaultdict(lambda: {"revenue": 0, "expense": 0})

        # 🔹 RECEITAS (Invoices pagas)
        invoices = Invoice.objects.filter(
            paid=True,
            paid_at__month=month,
            paid_at__year=year
        )

        for inv in invoices:
            day = inv.paid_at.day
            days[day]["revenue"] += float(inv.total_amount)

        # 🔹 EVENTOS (simplificado)
        events = Event.objects.all()
        for event in events:
            total = event.registration_fee * event.courseenrollment_set.count()
            # você pode melhorar isso depois com data real
            days[1]["revenue"] += float(total)

        # 🔹 DESPESAS
        outflows = Outflow.objects.filter(
            created_at__month=month,
            created_at__year=year
        )

        for out in outflows:
            day = out.created_at.day
            days[day]["expense"] += float(out.value or 0)

        # 🔹 SERIALIZA
        result = []
        for d in sorted(days.keys()):
            result.append({
                "day": d,
                "revenue": days[d]["revenue"],
                "expense": days[d]["expense"],
                "profit": days[d]["revenue"] - days[d]["expense"]
            })

        return Response(result)
    


class FinancialDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        month = int(request.GET.get("month"))
        year = int(request.GET.get("year"))
        financial_type = request.GET.get("type", "receitas")

        chart = []
        transactions = []
        total = 0

        # =====================================================
        # RECEITAS (RESUMO)
        # =====================================================

        if financial_type == "receitas":

            # MENSALIDADES PAGAS
            invoices = Invoice.objects.filter(
                billing_cycle__month=month,
                billing_cycle__year=year,
                paid=True
            )

            total_monthly = sum([
                float(i.total_amount)
                for i in invoices
            ])

            # EVENTOS
            enrollments = CourseEnrollment.objects.filter(
                enrollment_date__month=month,
                enrollment_date__year=year,
                paid=True
            )

            total_events = sum([
                float(e.event.registration_fee)
                for e in enrollments
            ])

            # OUTFLOWS EXTRA
            inflows = Inflow.objects.filter(
                created_at__month=month,
                created_at__year=year
            )

            total_inflows = sum([
                float(i.value or 0)
                for i in inflows
            ])

            total = (
                total_monthly +
                total_events +
                total_inflows
            )

            transactions = [
                {
                    "id": 1,
                    "description": f"Mensalidades {month}/{year}",
                    "category": "Mensalidades",
                    #"date": f"{year}-{month:02d}-01",
                    "date": date(year, month, 1),
                    "value": total_monthly
                },
                {
                    "id": 2,
                    "description": f"Eventos {month}/{year}",
                    "category": "Eventos",
                    #"date": f"{year}-{month:02d}-01",
                    "date": date(year, month, 1),
                    "value": total_events
                },
                {
                    "id": 3,
                    "description": f"Outras receitas {month}/{year}",
                    "category": "Outros",
                    #"date": f"{year}-{month:02d}-01",
                    "date": date(year, month, 1),
                    "value": total_inflows
                }
            ]

            # gráfico simples
            last_day = monthrange(year, month)[1]

            for day in range(1, last_day + 1):

                day_total = 0

                for invoice in invoices:
                    if invoice.due_date.day == day:
                        day_total += float(invoice.total_amount)

                chart.append({
                    "day": day,
                    "value": day_total
                })

        # =====================================================
        # MENSALIDADES
        # =====================================================

        elif financial_type == "mensalidades":

            invoices = Invoice.objects.filter(
                billing_cycle__month=month,
                billing_cycle__year=year
            ).select_related("karateca")

            total = sum([
                float(i.total_amount)
                for i in invoices
            ])

            last_day = monthrange(year, month)[1]

            for day in range(1, last_day + 1):

                daily_total = sum([
                    float(i.total_amount)
                    for i in invoices
                    if i.due_date.day == day
                ])

                chart.append({
                    "day": day,
                    "value": daily_total
                })

            for invoice in invoices.order_by("-due_date"):

                transactions.append({
                    "id": invoice.id,
                    "description": invoice.karateca.name,
                    "category": "Mensalidade",
                    "date": invoice.due_date,
                    "value": float(invoice.total_amount)
                })

        # =====================================================
        # DESPESAS
        # =====================================================

        elif financial_type == "despesas":

            outflows = Outflow.objects.filter(
                created_at__month=month,
                created_at__year=year
            ).select_related("expense")

            total = sum([
                float(o.value or 0)
                for o in outflows
            ])

            last_day = monthrange(year, month)[1]

            for day in range(1, last_day + 1):

                daily_total = sum([
                    float(o.value or 0)
                    for o in outflows
                    if o.created_at.day == day
                ])

                chart.append({
                    "day": day,
                    "value": daily_total
                })

            for outflow in outflows:

                transactions.append({
                    "id": outflow.id,
                    "description": outflow.name,
                    "category": outflow.expense.name,
                    "date": outflow.created_at.date(),
                    "value": float(outflow.value or 0)
                })

        # =====================================================
        # EVENTOS
        # =====================================================

        elif financial_type == "eventos":

            enrollments = CourseEnrollment.objects.filter(
                enrollment_date__month=month,
                enrollment_date__year=year
            ).select_related(
                "karateca",
                "event"
            )

            total = sum([
                float(e.event.registration_fee)
                for e in enrollments
            ])

            last_day = monthrange(year, month)[1]

            for day in range(1, last_day + 1):

                daily_total = sum([
                    float(e.event.registration_fee)
                    for e in enrollments
                    if e.enrollment_date.day == day
                ])

                chart.append({
                    "day": day,
                    "value": daily_total
                })

            for enrollment in enrollments:

                transactions.append({
                    "id": enrollment.id,
                    "description": enrollment.karateca.name,
                    "category": (
                        "Pago"
                        if enrollment.paid
                        else "Pendente"
                    ),
                    "date": enrollment.enrollment_date.date(),
                    "value": float(
                        enrollment.event.registration_fee
                    )
                })

        data = {
            "title": financial_type.capitalize(),
            "total": total,
            "chart": chart,
            "transactions": transactions
        }

        #serializer = FinancialDetailSerializer(data)

        #return Response(serializer.data)
        return Response(data)
    

class FinancialChartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        financial_type = request.GET.get("type")
        month = request.GET.get("month")
        year = request.GET.get("year")

        invoices = Invoice.objects.filter(
            due_date__month=month,
            due_date__year=year
        )

        # ================= FILTROS =================

        if financial_type == "receitas":

            invoices = invoices.filter(
                paid=True
            )

        elif financial_type == "mensalidades":

            invoices = invoices.filter(
                billing_cycle__isnull=False
            )

        elif financial_type in ["despesas", "eventos", "outros"]:

            invoices = Invoice.objects.none()

        # ================= TOTAL =================

        total = invoices.aggregate(
            total=Sum("total_amount")
        )["total"] or Decimal("0")

        # ================= GRÁFICO =================

        grouped = (
            invoices
            .annotate(day=ExtractDay("due_date"))
            .values("day")
            .annotate(value=Sum("total_amount"))
            .order_by("day")
        )

        chart = []

        for item in grouped:
            chart.append({
                "day": item["day"],
                "value": float(item["value"])
            })

        # ================= ITENS =================

        items = []

        for invoice in invoices.order_by("-due_date")[:50]:

            items.append({
                "description": f"Fatura #{invoice.id}",
                "category": financial_type,
                "value": float(invoice.total_amount or 0),
                "date": invoice.due_date.strftime("%Y-%m-%d")
            })

        return Response({
            "title": financial_type,
            "total": float(total),
            "chart": chart,
            "items": items
        })