from django.db import models
from graduations.models import Graduation
# ======================================================
# Modelo que representa uma Categoria de Exame
# (ex: Branca -> Amarela, Azul -> Verde, etc.)
# ======================================================
class ExamCategory(models.Model):
    """Define uma categoria de graduação, ex: Branca -> Amarela"""

    name_category = models.CharField(max_length=150)
    description = models.CharField(
        max_length=100,
        help_text="Descrição curta (ex: Branca para Amarela)"
    )

    def __str__(self):
        return self.name_category

