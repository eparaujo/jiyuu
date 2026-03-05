from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import TrainingAttendance
from .serializers import TrainingAttendanceSerializer
from rest_framework.permissions import IsAuthenticated
from .services import get_attendance_summary
from django.core.exceptions import ObjectDoesNotExist
from exams.models import Exam
from karatecas.models import Karateca
from .forms import AttendanceForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from senseis.models import Sensei
from django.http import HttpResponseForbidden
from dojos.models import Dojo
from . import services


class TrainingAttendanceCreateView(APIView):
    """
    Criação ou atualização de presença/falta.
    Se já existir (karateca + dojo + data), atualiza.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = TrainingAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        attendance, created = TrainingAttendance.objects.update_or_create(
            karateca=data["karateca"],
            dojo=data["dojo"],
            training_date=data["training_date"],
            defaults={"present": data["present"]},
        )

        return Response(
            TrainingAttendanceSerializer(attendance).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class TrainingAttendanceListView(APIView):
    """
    Lista presenças/faltas por karateca e período.
    Usado depois no dashboard.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        karateca_id = request.query_params.get("karateca")
        dojo_id = request.query_params.get("dojo")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        qs = TrainingAttendance.objects.all()

        if karateca_id:
            qs = qs.filter(karateca_id=karateca_id)

        if dojo_id:
            qs = qs.filter(dojo_id=dojo_id)

        if start_date:
            qs = qs.filter(training_date__gte=start_date)

        if end_date:
            qs = qs.filter(training_date__lte=end_date)

        serializer = TrainingAttendanceSerializer(qs, many=True)
        return Response(serializer.data)
    

class AttendanceSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # 1️⃣ vínculo User → Karateca
        if not hasattr(user, "karateka"):
            return Response(
                {"detail": "Usuário autenticado não possui vínculo com Karateca."},
                status=status.HTTP_400_BAD_REQUEST
            )

        karateca = user.karateka

        # 2️⃣ último exame FINALIZADO (aprovado ou não)
        last_finished_exam = (
            Exam.objects
            .filter(
                enrollments__karateca=karateca,
                status="FINALIZADO",
            )
            .order_by("-date")
            .first()
        )

        # 3️⃣ definir a data de corte
        start_date = None
        reset_by_exam = False

        if last_finished_exam:
            enrollment = last_finished_exam.enrollments.filter(
                karateca=karateca
            ).first()

            if enrollment and enrollment.approved:
                # ✅ aprovado → reinicia contagem
                start_date = last_finished_exam.date
                reset_by_exam = True
            else:
                # ❌ reprovado → buscar último aprovado
                last_approved_exam = (
                    Exam.objects
                    .filter(
                        enrollments__karateca=karateca,
                        enrollments__approved=True,
                        status="FINALIZADO",
                    )
                    .order_by("-date")
                    .first()
                )

                if last_approved_exam:
                    start_date = last_approved_exam.date
                    reset_by_exam = True

        # 4️⃣ presenças
        attendances = TrainingAttendance.objects.filter(
            karateca_id=karateca.id
        )

        if start_date:
            attendances = attendances.filter(
                training_date__gt=start_date
            )

        return Response({
            "karateka_id": karateca.id,
            "reset_by_exam": reset_by_exam,
            "start_date": start_date,
            "present_count": attendances.filter(present=True).count(),
            "absent_count": attendances.filter(present=False).count(),
        })
    
#-----------------------------------------
# # View para marcar a presença do aluno 
# ----------------------------------------
@login_required
def attendance_register_view(request):
    user = request.user

    # ===============================
    # 1️⃣ AUTORIZAÇÃO (UX PROFISSIONAL)
    # ===============================

    dojos = Dojo.objects.none()
    selected_dojo = None
    sensei = None

    # 🔐 Admin pode acessar todos os dojos
    if user.is_superuser:
        dojos = Dojo.objects.all().order_by("tradename")

    else:
        # 🔐 Usuário precisa ser Sensei
        try:
            sensei = user.sensei
        except ObjectDoesNotExist:
            return render(
                request,
                "attendance_not_allowed.html",
                {
                    "title": "Acesso não autorizado",
                    "message": "Seu usuário não está vinculado a um Sensei.",
                },
                status=403
            )

        # 🔐 Dojos vinculados ao Sensei (MANY TO MANY)
        dojos = Dojo.objects.filter(sensei=sensei).order_by("tradename")

        if not dojos.exists():
            return render(
                request,
                "attendance_not_allowed.html",
                {
                    "title": "Acesso restrito",
                    "message": "Você não está vinculado a nenhum Dojo.",
                },
                status=403
            )

    # ===============================
    # 2️⃣ DOJO SELECIONADO
    # ===============================

    selected_dojo_id = request.GET.get("dojo") or request.POST.get("dojo")

    if selected_dojo_id:
        selected_dojo = dojos.filter(id=selected_dojo_id).first()

    # ===============================
    # 3️⃣ LISTA DE KARATECAS
    # ===============================

    karatecas = Karateca.objects.none()

    if selected_dojo:
        karatecas = Karateca.objects.filter(
            dojo=selected_dojo,
            active="ATIVO"
        ).order_by("name")

    selected_date = request.GET.get("training_date") or request.POST.get("training_date")

    # ===============================
    # 4️⃣ SALVAR PRESENÇAS (POST)
    # ===============================

    if request.method == "POST" and selected_dojo and selected_date:
        for karateca in karatecas:
            present = request.POST.get(f"present_{karateca.id}") == "on"

            TrainingAttendance.objects.update_or_create(
                karateca=karateca,
                dojo=selected_dojo,
                training_date=selected_date,
                defaults={"present": present},
            )

        return redirect(
            f"{request.path}?dojo={selected_dojo.id}&training_date={selected_date}"
        )

    # ===============================
    # 5️⃣ RENDER DA TELA
    # ===============================

    return render(
        request,
        "attendance_form.html",
        {
            "dojos": dojos,
            "selected_dojo": selected_dojo,
            "karatecas": karatecas,
            "selected_date": selected_date,
        },
    )


#--------------------------------------------
# View para carência de exames
#--------------------------------------------
class GraduationEligibilityAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            karateca = request.user.karateka
        except ObjectDoesNotExist:
            return Response(
                {"detail": "Usuário não vinculado a Karateca"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = get_graduation_waiting_period(karateca)

        return Response({
            "karateca_id": karateca.id,
            "graduation": str(karateca.graduation),
            **data
        })