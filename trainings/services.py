from trainings.models import TrainingAttendance
from exams.models import ExamEnrollment
from datetime import date
from dateutil.relativedelta import relativedelta
from exams.models import Exam, ExamEnrollment
from karatecas.models import Karateca
from datetime import date
from dateutil.relativedelta import relativedelta
from graduations.models import Graduation


def get_last_exam_date(karateca):
    """
    Retorna a data do último exame válido do karateca.
    Exame válido = CONFIRMADO ou FINALIZADO.
    """
    enrollment = (
        ExamEnrollment.objects
        .filter(
            karateca=karateca,
            exam__status__in=["CONFIRMADO", "FINALIZADO"]
        )
        .select_related("exam")
        .order_by("-exam__date")
        .first()
    )

    return enrollment.exam.date if enrollment else None

def get_attendance_summary(karateca):
    """
    Retorna presenças e faltas a partir do último exame válido.
    """
    last_exam_date = get_last_exam_date(karateca)

    qs = TrainingAttendance.objects.filter(karateca=karateca)

    if last_exam_date:
        qs = qs.filter(training_date__gt=last_exam_date)

    present_count = qs.filter(present=True).count()
    absent_count = qs.filter(present=False).count()

    return {
        "from_date": last_exam_date,
        "present": present_count,
        "absent": absent_count,
    }

#-----------------------------------------------------------
# função para verificação e cálculo de carência para exames
#-----------------------------------------------------------
def get_graduation_waiting_period(karateca: Karateca):
    """
    Retorna informações de carência por faixa:
    - data do último exame aprovado
    - meses exigidos
    - meses cumpridos
    - se está apto ou não
    """

    # Último exame FINALIZADO + APROVADO
    last_exam = (
        Exam.objects
        .filter(
            enrollments__karateca=karateca,
            enrollments__approved=True,
            status="FINALIZADO"
        )
        .order_by("-date")
        .first()
    )

    if not last_exam:
        return {
            "has_previous_exam": False,
            "eligible": True,  # primeiro exame não tem carência
            "required_months": 0,
            "elapsed_months": 0,
            "remaining_months": 0,
            "last_exam_date": None,
        }

    graduation = karateca.graduation

    required_months = graduation.min_months if graduation else 0

    today = date.today()
    elapsed = relativedelta(today, last_exam.date)
    elapsed_months = elapsed.years * 12 + elapsed.months

    remaining = max(required_months - elapsed_months, 0)

    return {
        "has_previous_exam": True,
        "eligible": remaining == 0,
        "required_months": required_months,
        "elapsed_months": elapsed_months,
        "remaining_months": remaining,
        "last_exam_date": last_exam.date,
    }

#--------------------------------------------------------
# função para verificar habilitação para o próximo exame
#--------------------------------------------------------
def can_do_exam(karateca):
    """
    Verifica se o karateca pode realizar um novo exame,
    respeitando a carência mínima da graduação atual.
    """

    # 🔹 Último exame APROVADO do karateca
    last_enrollment = (
        ExamEnrollment.objects
        .filter(
            karateca=karateca,
            approved=True
        )
        .select_related("exam", "current_graduation")
        .order_by("-exam__date")
        .first()
    )

    # 🔹 Nunca fez exame → pode fazer
    if not last_enrollment:
        return True, None

    graduation = last_enrollment.current_graduation

    # 🔹 Segurança extra (caso raro)
    if not graduation:
        return True, None

    min_months = graduation.min_months
    last_exam_date = last_enrollment.exam.date

    # 🔹 Data mínima permitida para novo exame
    allowed_date = last_exam_date + relativedelta(months=min_months)

    today = date.today()

    if today >= allowed_date:
        return True, None

    # 🔹 Ainda em carência
    remaining = relativedelta(allowed_date, today)

    message = (
        f"Carência não cumprida para a graduação {graduation.name}. "
        f"Faltam {remaining.months} mês(es) e {remaining.days} dia(s)."
    )

    return False, message