from django.urls import path
from . import views
from trainings.views import CreateTrainingCheckinSessionAPIView

urlpatterns = [
    path("api/v1/trainings/attendance/", views.TrainingAttendanceCreateView.as_view(), name="training-attendance-create"),
    path("api/v1/attendance/list/", views.TrainingAttendanceListView.as_view(), name="training-attendance-list"),
    path("api/v1/attendance/summary/", views.AttendanceSummaryAPIView.as_view(), name="attendance-summary"),
    path("api/v1/attendance/register/", views.attendance_register_view, name="attendance_register"),
    path("api/v1/trainings/checkin/create-session/", CreateTrainingCheckinSessionAPIView.as_view(),  name="create_training_checkin_session"),
    #endpoint para mobile, aluno registra presença via QR Code
    path("api/v1/attendance/register/", views.RegisterAttendanceByQrAPIView.as_view(), name="attendance-register"),
]