from django.urls import path
from . import views

urlpatterns = [
    path('classes/list/', views.ClassListView.as_view(), name='class_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('classes/create/', views.ClassCreateView.as_view(), name='class_create'),
    path('classes/<int:pk>/detail/', views.ClassDetailView.as_view(), name='class_detail'),
    path('classes/<int:pk>/update/', views.ClassUpdateView.as_view(), name='class_update'),
    path('classes/<int:pk>/delete/', views.ClassDeleteView.as_view(), name='class_delete'),
]