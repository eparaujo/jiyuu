from datetime import date
from dateutil.relativedelta import relativedelta

from .models import Exam, ExamEnrollment
from graduations.models import Graduation


def can_do_exam(*, karateca, exam: Exam, category):
    """
    Verifica se um karateca pode se inscrever em um exame
    para uma determinada categoria.
    """

    # ==================================================
    # 1. Karateca precisa ter graduação atual
    # ==================================================
    current_graduation = getattr(karateca, "current_graduation", None)
    if not current_graduation:
        return False, "Karateca não possui graduação atual."

    # ==================================================
    # 2. Categoria precisa fazer parte do exame
    # ==================================================
    if not exam.categories.filter(id=category.id).exists():
        return False, "Categoria não pertence a este exame."

    # ==================================================
    # 3. Graduação compatível com a categoria
    # (ex: Amarela -> Laranja)
    # ==================================================
    if category.from_graduation != current_graduation:
        return (
            False,
            f"Graduação incompatível. Atual: {current_graduation.name}."
        )

    # ==================================================
    # 4. Não permitir dupla inscrição
    # ==================================================
    if ExamEnrollment.objects.filter(
        exam=exam,
        karateca=karateca
    ).exists():
        return False, "Karateca já está inscrito neste exame."

    # ==================================================
    # 5. Verificar carência (tempo mínimo entre exames)
    # ==================================================
    last_approved_exam = (
        ExamEnrollment.objects
        .filter(
            karateca=karateca,
            approved=True,
            exam__status="FINALIZADO"
        )
        .select_related("exam")
        .order_by("-exam__date")
        .first()
    )

    if last_approved_exam and category.min_months_interval:
        min_date = last_approved_exam.exam.date + relativedelta(
            months=category.min_months_interval
        )

        if exam.date < min_date:
            return (
                False,
                f"Carência não cumprida. Próximo exame permitido após "
                f"{min_date.strftime('%d/%m/%Y')}."
            )

    # ==================================================
    # ✅ Todas as regras passaram
    # ==================================================
    return True, "Karateca apto para o exame."