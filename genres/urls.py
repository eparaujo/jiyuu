from django.urls import path
from . import views

urlpatterns = [
    path('genres/list/', views.GenreListView.as_view(), name='genre_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('genres/create/', views.GenreCreateView.as_view(), name='genre_create'),
    path('genres/<int:pk>/detail/', views.GenreDetailView.as_view(), name='genre_detail'),
    path('genres/<int:pk>/update/', views.GenreUpdateView.as_view(), name='genre_update'),
    path('genres/<int:pk>/delete/', views.GenreDeleteView.as_view(), name='genre_delete'),
    # endpoint usado pelo flutter
    path('api/v1/genres/', views.GenreListAPI.as_view(), name='api_genres'),
]