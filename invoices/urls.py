from django.urls import path
from . import views

urlpatterns = [
    path('invoice/list/', views.InvoiceListView.as_view(), name='invoice_list'),
    path('generate/', views.generate_invoices_view, name='generate_invoices'),
    path('close/', views.close_cycle_view, name='close_cycle'),
    path('reset/', views.reset_cycle_view, name='reset_cycle'),
    path('invoice/<int:pk>/', views.InvoiceDetailView.as_view(), name='invoice_detail'),
    path('invoice/<int:pk>/paid/', views.mark_invoice_paid, name='invoice_mark_paid'),
]
