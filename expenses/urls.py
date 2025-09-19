from django.urls import path
from . import views

urlpatterns = [
    path('expenses/list/', views.ExpenseListView.as_view(), name='expense_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('expenses/create/', views.ExpenseCreateView.as_view(), name='expense_create'),
    path('expenses/<int:pk>/detail/', views.ExpenseDetailView.as_view(), name='expense_detail'),
    path('expenses/<int:pk>/update/', views.ExpenseUpdateView.as_view(), name='expense_update'),
    path('expenses/<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='expense_delete'),
]