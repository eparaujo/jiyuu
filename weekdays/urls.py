from django.urls import path
from . import views

urlpatterns = [
    path('weekdays/list/', views.WeekdaysListView.as_view(), name='weekdays_list'), # a utilização do name aqui, serve por exemplo para ser usada no HTML no método de busca
    path('weekdays/create/', views.WeekdaysCreateView.as_view(), name='weekdays_create'),
    path('weekdays/<int:pk>/detail/', views.WeekdaysDetailView.as_view(), name='weekdays_detail'),
    path('weekdays/<int:pk>/update/', views.WeekdaysUpdateView.as_view(), name='weekdays_update'),
    path('weekdays/<int:pk>/delete/', views.WeekdaysDeleteView.as_view(), name='weekdays_delete'),
]