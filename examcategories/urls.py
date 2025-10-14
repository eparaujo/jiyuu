from django.urls import path
from . import views

urlpatterns = [
    path('examcategories/list/', views.ExamCategoryListView.as_view(), name='examcategory_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('examcategories/create/', views.ExamCategoryCreateView.as_view(), name='examcategory_create'),
    path('examcategories/<int:pk>/detail/', views.ExamCategoryDetailView.as_view(), name='examcategory_detail'),
    path('examcategories/<int:pk>/delete/', views.ExamCategoryDeleteView.as_view(), name='examcategory_delete'),
    path('examcategories/<int:pk>/update/', views.ExamCategoryUpdateView.as_view(), name='examcategory_update'),

 # urls para serem usadas via API no flutter
    path('api/v1/examcategories/<int:pk>/', views.ExamCategoryRetrieveUpdateDestroyAPIView.as_view(), name='exam-categories-retrieve-api'),
    path('api/v1/list/<int:pk>/', views.ExamCategoryListAPIView.as_view(), name='exam-category-create-list-api'),
]