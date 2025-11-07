from django.urls import path
from . import views

urlpatterns = [
    path('events/list/', views.EventListView.as_view(), name='event_list'),
    path('events/create/', views.EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/detail/', views.EventDetailView.as_view(), name='event_detail'),
    path('events/<int:pk>/update/', views.EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', views.EventDeleteView.as_view(), name='event_delete'),

    # Inscrição e pagamento
    path('events/<int:event_id/enrollment/', views.EventEnrollmentFormView, name='event_enrollment'),
    path('events/payment/<int:enrollment_id>/toggle/', views.toggle_payment_status, name='toggle_payment_status'),

    # API
    path('api/events/', views.EventListAPI.as_view(), name='api_event_list'),
    path('api/enrollments/', views.CourseEnrollmentCreateAPI.as_view(), name='api_course_enrollment'),
]
