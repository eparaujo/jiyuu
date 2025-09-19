# dashboards/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils.timezone import now
from django.db.models import Q

# Importa models usados para cálculo do dashboard
from exams.models import Exam, ExamEnrollment, ExamResult
from events.models import Event
from dojos.models import Dojo
from dashboards.models import Dashboard

# 🔹 Importa Karateca para contar alunos ativos
from karatecas.models import Karateca


def is_enrollment_approved(enrollment):
    """
    Regra de aprovação baseada nos requisitos do exame.
    Retorna True se o aluno cumprir todos requisitos com nota >= min_score.
    """
    requirements = enrollment.exam.requirements.all()
    results = {r.subject_id: r.score for r in enrollment.results.all()}

    for req in requirements:
        if req.subject_id not in results:
            return False
        if results[req.subject_id] < req.min_score:
            return False
    return True


def build_upcoming_events_for_dojo(dojo):
    """
    Retorna lista de eventos futuros relevantes para o dojo informado.
    Inclui:
      - eventos globais (sem organizer ou externos)
      - eventos cujo organizer corresponde ao dojo
    """
    today = now().date()
    upcoming = Event.objects.filter(date__gte=today).order_by("date")
    events_list = []

    for e in upcoming:
        org = (e.organizer or "").strip()
        include = False

        if not org:
            include = True
        else:
            matching_dojos = Dojo.objects.filter(
                Q(razaosocial__iexact=org) | Q(tradename__iexact=org)
            )
            if matching_dojos.exists():
                include = matching_dojos.filter(id=dojo.id).exists()
            else:
                include = True

        if include:
            events_list.append(
                {
                    "id": e.id,
                    "name": e.name,
                    "date": e.date.isoformat(),
                    "description": e.description,
                    "organizer": e.organizer or "",
                }
            )

    return events_list


def update_dashboard(dojo):
    """
    Atualiza os campos do Dashboard para o dojo fornecido.
    Calcula:
     - active_students (karatecas ativos)
     - último exame (data, participantes, aprovados, lista de alunos)
     - próximo exame (data, inscritos, lista de nomes)
     - upcoming_events (eventos relevantes)
    """
    dashboard, _ = Dashboard.objects.get_or_create(dojo=dojo)

    # ---------- 🔹 Contagem de alunos ativos ----------
    # Busca Karatecas vinculados ao dojo, cujo campo active == "ATIVO"
    active_count = Karateca.objects.filter(dojo=dojo, active="ATIVO").count()
    dashboard.active_students = active_count

    # ---------- Último exame ----------
    last_exam = Exam.objects.filter(dojo=dojo).order_by("-date").first()
    if last_exam:
        dashboard.last_exam_date = last_exam.date
        dashboard.last_exam_participants = last_exam.enrollments.count()

        approved_count = sum(1 for e in last_exam.enrollments.all() if is_enrollment_approved(e))
        dashboard.last_exam_approved = approved_count

        dashboard.last_exam_students = [
            {
                "id": e.karateca.id,
                "name": e.karateca.name,
                "approved": is_enrollment_approved(e),
            }
            for e in last_exam.enrollments.all()
        ]
    else:
        dashboard.last_exam_date = None
        dashboard.last_exam_participants = 0
        dashboard.last_exam_approved = 0
        dashboard.last_exam_students = []

    # ---------- Próximo exame ----------
    today = now().date()
    next_exam = Exam.objects.filter(dojo=dojo, date__gte=today).order_by("date").first()
    if next_exam:
        dashboard.next_exam_date = next_exam.date
        dashboard.next_exam_registered = next_exam.enrollments.count()
        dashboard.next_exam_students = [
            {"id": e.karateca.id, "name": e.karateca.name}
            for e in next_exam.enrollments.all()
        ]
        dashboard.next_exam_name = f"Exame {next_exam.date.isoformat()}"
    else:
        dashboard.next_exam_date = None
        dashboard.next_exam_registered = 0
        dashboard.next_exam_students = []
        dashboard.next_exam_name = ""

    # ---------- Eventos futuros ----------
    dashboard.upcoming_events = build_upcoming_events_for_dojo(dojo)

    # Salva alterações
    dashboard.save()


# --------------------------- Signals ---------------------------
@receiver(post_save, sender=Exam)
@receiver(post_delete, sender=Exam)
@receiver(post_save, sender=ExamEnrollment)
@receiver(post_delete, sender=ExamEnrollment)
@receiver(post_save, sender=ExamResult)
@receiver(post_delete, sender=ExamResult)
def refresh_dashboard_for_exam_related(sender, instance, **kwargs):
    """
    Atualiza dashboard quando Exame/Inscrição/Resultado é criado, alterado ou removido.
    """
    dojo = None
    if isinstance(instance, Exam):
        dojo = instance.dojo
    elif isinstance(instance, ExamEnrollment):
        dojo = instance.exam.dojo
    elif isinstance(instance, ExamResult):
        dojo = instance.enrollment.exam.dojo

    if dojo:
        update_dashboard(dojo)


@receiver(post_save, sender=Event)
@receiver(post_delete, sender=Event)
def refresh_dashboard_for_event(sender, instance, **kwargs):
    """
    Atualiza dashboards quando um Evento é criado/alterado/excluído.
    - Se for global/external -> atualiza todos dashboards
    - Se for de um dojo específico -> atualiza apenas os dashboards daquele dojo
    """
    org = (instance.organizer or "").strip()

    if not org:
        for dashboard in Dashboard.objects.all():
            update_dashboard(dashboard.dojo)
        return

    matching_dojos = Dojo.objects.filter(
        Q(razaosocial__iexact=org) | Q(tradename__iexact=org)
    )

    if matching_dojos.exists():
        for dojo in matching_dojos:
            update_dashboard(dojo)
    else:
        for dashboard in Dashboard.objects.all():
            update_dashboard(dashboard.dojo)
