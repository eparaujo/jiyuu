from dateutil.relativedelta import relativedelta

from .models import Exam, ExamEnrollment, ExamResult
from graduations.models import Graduation


def get_next_graduation(current_graduation):
    """
    Retorna a próxima graduação conforme a sequência definida
    no campo Graduation.order.
    """

    if not current_graduation:
        return None

    return (
        Graduation.objects
        .filter(
            order__gt=current_graduation.order
        )
        .order_by("order")
        .first()
    )


def can_do_exam(
    *,
    karateca,
    exam: Exam,
    category,
    break_grace_period=False):
    """
    Verifica se o karateca pode se inscrever em um exame
    para determinada categoria.

    Retorna:
        (True, mensagem)
        ou
        (False, mensagem)
    """

    # ==================================================
    # 1. Graduação atual
    # ==================================================

    current_graduation = karateca.graduation

    if not current_graduation:
        return (
            False,
            "Karateca não possui graduação atual."
        )

    # ==================================================
    # 2. Categoria pertence ao exame?
    # ==================================================

    if not exam.categories.filter(
        id=category.id
    ).exists():

        return (
            False,
            "A categoria selecionada não pertence a este exame."
        )

    # ==================================================
    # 3. Categoria corresponde à próxima graduação?
    # ==================================================

    next_graduation = get_next_graduation(
        current_graduation
    )

    if not next_graduation:

        return (
            False,
            "Não existe uma próxima graduação cadastrada "
            "para este karateca."
        )

    if category.to_graduation != next_graduation:

        return (
            False,
            (
                f"A categoria selecionada não corresponde "
                f"à próxima graduação do karateca. "
                f"Graduação atual: {current_graduation.name}. "
                f"Próxima graduação esperada: "
                f"{next_graduation.name}."
            )
        )

    # ==================================================
    # 4. Inscrição duplicada
    # ==================================================

    if ExamEnrollment.objects.filter(
        exam=exam,
        karateca=karateca
    ).exists():

        return (
            False,
            "Karateca já está inscrito neste exame."
        )

    # ==================================================
    # 5. Data da graduação
    # ==================================================

    if not karateca.graduation_date:

        return (
            False,
            (
                "A data da graduação atual não está "
                "cadastrada para este karateca."
            )
        )

    # ==================================================
    # 6. Carência
    # ==================================================

    eligible_date = (
        karateca.graduation_date
        + relativedelta(
            months=current_graduation.min_months
        )
    )

    # ==================================================
    # 7. Quebra de carência
    # ==================================================

    if exam.date < eligible_date:

        if not break_grace_period:

            return (
                False,
                (
                    f"Carência não cumprida. "
                    f"Graduação atual: "
                    f"{current_graduation.name}. "
                    f"Carência mínima: "
                    f"{current_graduation.min_months} meses. "
                    f"Elegível a partir de "
                    f"{eligible_date.strftime('%d/%m/%Y')}."
                )
            )

    # ==================================================
    # 8. Apto
    # ==================================================

    return (
        True,
        "Karateca apto para o exame."
    )



def calculate_exam_approval(enrollment):
    """
    Calcula se o karateca foi aprovado no exame.

    Regra:
    - Todas as matérias configuradas para a categoria do karateca
      precisam possuir resultado.
    - A nota obtida precisa ser >= min_score.
    - max_score não participa da regra de aprovação.
    """

    requirements = enrollment.exam.requirements.filter(
        category=enrollment.category
    )

    # Sem requisitos configurados, não aprova automaticamente.
    if not requirements.exists():
        enrollment.approved = False
        enrollment.save(update_fields=["approved"])
        return False

    for requirement in requirements:

        result = ExamResult.objects.filter(
            enrollment=enrollment,
            subject=requirement.subject
        ).first()

        # Ainda não existe nota para a matéria
        if not result:
            enrollment.approved = False
            enrollment.save(update_fields=["approved"])
            return False

        # A nota mínima não foi atingida
        if result.score < requirement.min_score:
            enrollment.approved = False
            enrollment.save(update_fields=["approved"])
            return False

    # Todas as matérias atingiram o mínimo
    enrollment.approved = True
    enrollment.save(update_fields=["approved"])

    return True