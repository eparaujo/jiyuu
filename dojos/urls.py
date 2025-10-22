from django.urls import path
from . import views

urlpatterns = [
    path('dojos/list/', views.DojoListView.as_view(), name='dojo_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('dojos/create/', views.DojoCreateView.as_view(), name='dojo_create'),
    path('dojos/<int:pk>/detail/', views.DojoDetailView.as_view(), name='dojo_detail'),
    path('dojos/<int:pk>/update/', views.DojoUpdateView.as_view(), name='dojo_update'),
    path('dojos/<int:pk>/delete/', views.DojoDeleteView.as_view(), name='dojo_delete'),
    # endpoint a ser usado pelo flutter
    path('api/v1/dojos/', views.DojoListAPI.as_view(), name='api_genres'),

] 