from rest_framework.views import APIView
from rest_framework.response import Response
from .services import get_financial_metrics
from invoices.models import Invoice
from outflows.models import Outflow
from events.models import Event

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
    

# api/v1/dashboard/financial/details/

class FinancialDetailsAPIView(APIView):

    def get(self, request):
        kind = request.GET.get("type")  # receitas | despesas | mensalidades | eventos

        if kind == "receitas":
            data = Invoice.objects.filter(paid=True)

            return Response([
                {
                    "title": str(i.karateca),
                    "value": float(i.total_amount),
                    "date": i.paid_at
                } for i in data
            ])

        elif kind == "despesas":
            data = Outflow.objects.all()

            return Response([
                {
                    "title": o.name,
                    "value": float(o.value or 0),
                    "date": o.created_at
                } for o in data
            ])

        return Response([])    