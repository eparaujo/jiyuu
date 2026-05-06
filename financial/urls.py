from django.urls import path
from .views import FinancialDashboardAPIView

urlpatterns = [
    path('api/v1/dashboard/', FinancialDashboardAPIView.as_view()),
]