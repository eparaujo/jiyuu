from django.urls import path
from . import views

urlpatterns = [
    path("api/v1/dashboard/", views.DashboardListView.as_view(), name="dashboard_list"),
    path("dashboards/create/", views.DashboardCreateView.as_view(), name="dashboard_create"),
    path("dashboards/<int:pk>/", views.DashboardDetailView.as_view(), name="dashboard_detail"),
    path("dashboards/<int:pk>/update/", views.DashboardUpdateView.as_view(), name="dashboard_update"),
    path("dashboards/<int:pk>/delete/", views.DashboardDeleteView.as_view(), name="dashboard_delete"),
    # endpoint externo para o flutter
    path("api/v1/dashboardapi/", views.DashboardAPIView.as_view(), name="dashboard_api"),    
]
