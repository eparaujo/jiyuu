from django.urls import path
from . import views

urlpatterns = [
    path('karatecas/list/', views.KaratecaListView.as_view(), name='karateca_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('karatecas/create/', views.KaratecaCreateView.as_view(), name='karateca_create'),
    path('karatecas/<int:pk>/detail/', views.KaratecaDetailView.as_view(), name='karateca_detail'),
    path('karatecas/<int:pk>/update/', views.KaratecaUpdateView.as_view(), name='karateca_update'),
    path('karatecas/<int:pk>/delete/', views.KaratecaDeleteView.as_view(), name='karateca_delete'),
]