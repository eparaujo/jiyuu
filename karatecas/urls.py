from django.urls import path
from . import views

urlpatterns = [
    path('karatecas/list/', views.KaratecaListView.as_view(), name='karateca_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('karatecas/create/', views.KaratecaCreateView.as_view(), name='karateca_create'),
    path('karatecas/<int:pk>/detail/', views.KaratecaDetailView.as_view(), name='karateca_detail'),
    path('karatecas/<int:pk>/update/', views.KaratecaUpdateView.as_view(), name='karateca_update'),
    path('karatecas/<int:pk>/delete/', views.KaratecaDeleteView.as_view(), name='karateca_delete'),
    # endpoint para uso do app no cadastro de Karatecas
    path('api/v1/karatecas/', views.KaratecaCreateListAPIView.as_view(), name='karateca_create_list_api_view'),
    path('api/v1/karatecas/<int:pk>/', views.KaratecaRetrieveUpdateDestroyAPIView.as_view(), name='karateca_retrieve_update_api_view'),
    path('api/v1/register/', views.PublicKaratekaRegisterView.as_view(), name='public_karateca_register'),
    path('api/v1/karatecas/me/graduation-status/', views.KaratecaGraduationStatusAPIView.as_view(), name='karateca_graduation_status'),
    path('karatecas/<int:pk>/set-password/', views.set_karateca_password, name='karateca_set_password'),#resetar/gravar password do aluno
    path('api/v1/dashboard/totalkaratecas/', views.StudentStatsAPIView.as_view(), name='karateca_total')
] 