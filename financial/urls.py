from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/dashboard/', views.FinancialDashboardAPIView.as_view()),
    path('api/v1/dashboard/financial/timeseries/', views.FinancialTimeseriesAPIView.as_view()),
    path('api/v1/dashboard/financial/details/', views.FinancialDetailsAPIView.as_view()),
]