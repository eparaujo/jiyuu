from django.urls import path
from . import views

urlpatterns = [
    path('categories/list/', views.CategoryListView.as_view(), name='category_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/detail/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),
]