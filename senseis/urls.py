from django.urls import path
from . import views

urlpatterns = [
    path('senseis/list/', views.SenseiListView.as_view(), name='sensei_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('senseis/create/', views.SenseiCreateView.as_view(), name='sensei_create'),
    path('senseis/<int:pk>/detail/', views.SenseiDetailView.as_view(), name='sensei_detail'),
    path('senseis/<int:pk>/update/', views.SenseiUpdateView.as_view(), name='sensei_update'),
    path('senseis/<int:pk>/delete/', views.SenseiDeleteView.as_view(), name='sensei_delete'),
]