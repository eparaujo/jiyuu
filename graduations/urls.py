from django.urls import path
from . import views

urlpatterns = [
    path('graduations/list/', views.GraduationListView.as_view(), name='graduation_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('graduations/create/', views.GraduationCreateView.as_view(), name='graduation_create'),
    path('graduations/<int:pk>/detail/', views.GraduationDetailView.as_view(), name='graduation_detail'),
    path('graduations/<int:pk>/update/', views.GraduationUpdateView.as_view(), name='graduation_update'),
    path('graduations/<int:pk>/delete/', views.GraduationDeleteView.as_view(), name='graduation_delete'),
]