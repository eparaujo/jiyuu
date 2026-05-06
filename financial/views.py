from rest_framework.views import APIView
from rest_framework.response import Response
from .services import get_financial_metrics

class FinancialDashboardAPIView(APIView):
    def get(self, request):
        month = request.GET.get("month")
        year = request.GET.get("year")

        data = get_financial_metrics(
            month=int(month) if month else None,
            year=int(year) if year else None
        )

        return Response(data)