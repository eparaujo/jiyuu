from django.urls import path
from . import views

urlpatterns = [
    path('katas/list/', views.KataListView.as_view(), name='kata_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('katas/create/', views.KataCreateView.as_view(), name='kata_create'),
    path('katas/<int:pk>/detail/', views.KataDetailView.as_view(), name='kata_detail'),
    path('katas/<int:pk>/update/', views.KataUpdateView.as_view(), name='kata_update'),
    path('katas/<int:pk>/delete/', views.KataDeleteView.as_view(), name='kata_delete'),
]