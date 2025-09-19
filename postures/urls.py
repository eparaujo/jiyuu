from django.urls import path
from . import views

urlpatterns = [
    path('postures/list/', views.PostureListView.as_view(), name='posture_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('postures/create/', views.PostureCreateView.as_view(), name='posture_create'),
    path('postures/<int:pk>/detail/', views.PostureDetailView.as_view(), name='posture_detail'),
    path('postures/<int:pk>/update/', views.PostureUpdateView.as_view(), name='posture_update'),
    path('katposturesas/<int:pk>/delete/', views.PostureDeleteView.as_view(), name='posture_delete'),
]