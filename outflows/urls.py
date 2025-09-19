from django.urls import path
from . import views

urlpatterns = [
    path('outflows/list/', views.OutflowListView.as_view(), name='outflow_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('outflows/create/', views.OutflowCreateView.as_view(), name='outflow_create'),
    path('outflows/<int:pk>/detail/', views.OutflowDetailView.as_view(), name='outflow_detail'),
]