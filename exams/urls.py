# exams/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('exams/list/', views.ExamListView.as_view(), name='exam_list'),
    path('exams/create/', views.ExamCreateView.as_view(), name='exam_create'),
    path('exams/<int:pk>/detail/', views.ExamDetailView.as_view(), name='exam_detail'),
    path('exams/<int:pk>/update/', views.ExamUpdateView.as_view(), name='exam_update'),
    path('exams/<int:pk>/delete/', views.ExamDeleteView.as_view(), name='exam_delete'),

    path('subjects/list/', views.ExamSubjectListView.as_view(), name='subject_list'),
    path('subjects/create/', views.ExamSubjectCreateView.as_view(), name='subject_create'),
    path('subjects/<int:pk>/detail/', views.ExamSubjectDetailView.as_view(), name='subject_detail'),
    path('subjects/<int:pk>/update/', views.ExamSubjectUpdateView.as_view(), name='subject_update'),
    path('subjects/<int:pk>/delete/', views.ExamSubjectDeleteView.as_view(), name='subject_delete'),

    path('requirements/list/', views.ExamRequirementListView.as_view(), name='requirement_list'),
    path('requirements/create/', views.ExamRequirementCreateView.as_view(), name='requirement_create'),
    path('requirements/<int:pk>/detail/', views.ExamRequirementDetailView.as_view(), name='requirement_detail'),
    path('requirements/<int:pk>/update/', views.ExamRequirementUpdateView.as_view(), name='requirement_update'),
    path('requirements/<int:pk>/delete/', views.ExamRequirementDeleteView.as_view(), name='requirement_delete'),

    path('enrollments/list/', views.ExamEnrollmentListView.as_view(), name='enrollment_list'),
    path('enrollments/create/', views.ExamEnrollmentCreateView.as_view(), name='enrollment_create'),
    path('enrollments/<int:pk>/detail/', views.ExamEnrollmentDetailView.as_view(), name='enrollment_detail'),
    path('enrollments/<int:pk>/update/', views.ExamEnrollmentUpdateView.as_view(), name='enrollment_update'),
    path('enrollments/<int:pk>/delete/', views.ExamEnrollmentDeleteView.as_view(), name='enrollment_delete'),

    path('results/list/', views.ExamResultListView.as_view(), name='result_list'),
    path('results/create/', views.ExamResultCreateView.as_view(), name='result_create'),
    path('results/<int:pk>/detail/', views.ExamResultDetailView.as_view(), name='result_detail'),
    path('results/<int:pk>/update/', views.ExamResultUpdateView.as_view(), name='result_update'),
    path('results/<int:pk>/delete/', views.ExamResultDeleteView.as_view(), name='result_delete'),
]
