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
    to_graduation = models.ForeignKey(
    Graduation,
    on_delete=models.PROTECT,
    related_name="exam_target_categories",
    null=True,
    blank=True
)

    def __str__(self):
        return self.name_category

