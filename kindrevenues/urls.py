from django.urls import path
from . import views

urlpatterns = [
    path('kindrevenues/list/', views.KindRevenueListView.as_view(), name='kindrevenue_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('kindrevenues/create/', views.KindRevenueCreateView.as_view(), name='kindrevenue_create'),
    path('kindrevenues/<int:pk>/detail/', views.KindRevenueDetailView.as_view(), name='kindrevenue_detail'),
    path('kindrevenues/<int:pk>/update/', views.KindRevenueUpdateView.as_view(), name='kindrevenue_update'),
    path('kindrevenues/<int:pk>/delete/', views.KindRevenueDeleteView.as_view(), name='kindrevenue_delete'),
]