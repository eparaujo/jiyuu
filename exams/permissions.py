# exams/permissions.py
from rest_framework.permissions import BasePermission
from dojos.models import DojoMembership
from dojos.choices import DojoRole
from exams.models import Exam, ExamEnrollment


class IsOwnerOrExaminer(BasePermission):
    """
    Permite acesso apenas para OWNER, EXAMINER ou ADMIN
    do dojo ao qual o exame (ou inscrição) pertence.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        dojo = None

        # 🔹 Caso 1: endpoint de Enrollment (/enrollments/<pk>/)
        enrollment_id = view.kwargs.get("pk")
        if enrollment_id and "enrollments" in request.path:
            try:
                enrollment = ExamEnrollment.objects.select_related("exam__dojo").get(
                    pk=enrollment_id
                )
                dojo = enrollment.exam.dojo
            except ExamEnrollment.DoesNotExist:
                return False

        # 🔹 Caso 2: endpoint de Exam (/exams/<pk>/)
        exam_id = view.kwargs.get("pk")
        if exam_id and "exams" in request.path:
            try:
                exam = Exam.objects.select_related("dojo").get(pk=exam_id)
                dojo = exam.dojo
            except Exam.DoesNotExist:
                return False

        if not dojo:
            return False

        return DojoMembership.objects.filter(
            user=request.user,
            dojo=dojo,
            role__in=[
                DojoRole.OWNER,
                DojoRole.EXAMINER,
                DojoRole.ADMIN,
            ],
            is_active=True,
        ).exists()