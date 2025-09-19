from django.urls import path
from . import views

urlpatterns = [
    path('events/list/', views.EventListView.as_view(), name='event_list'), 
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/detail/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),
    
    #aqui abaixo, são as urls a serem usadas em chamadas via API, assim o fullstack fica completo podendo também ser utilizado para uso via API
    #path('api/v1/login/', views.EmailLoginView.as_view(), name='email_login'),
    #path('api/v1/events/<int:pk>/', views.EventRetrieveUpdateDestroyApiView.as_view(), name='event-detail-api-view'),
    #path('api/v1/events/register/', views.EventRegisterAPIView.as_view(), name='event-register'),
]