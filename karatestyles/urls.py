from django.urls import path
from . import views

urlpatterns = [
    path('karatestyles/list/', views.KarateStyleListView.as_view(), name='karatestyle_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('karatestyles/create/', views.KarateStyleCreateView.as_view(), name='karatestyle_create'),
    path('karatestyles/<int:pk>/detail/', views.KarateStyleDetailView.as_view(), name='karatestyle_detail'),
    path('karatestyles/<int:pk>/update/', views.KarateStyleUpdateView.as_view(), name='karatestyle_update'),
    path('karatestyles/<int:pk>/delete/', views.KarateStyleDeleteView.as_view(), name='karatestyle_delete'),
] 