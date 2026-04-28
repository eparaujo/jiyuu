from django.db import models
from kindrevenues.models import KindRevenue
from datetime import datetime
from django.core.exceptions import ValidationError


def validate_day_month(value):
    """Valida se o valor está no formato correto de dia e mês."""
    try:
        datetime.strptime(value, "%d-%m")  # ✅ corrigido
    except ValueError:
        raise ValidationError("O valor deve estar no formato DD-MM (por exemplo, 25-12).")


class Revenue(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(KindRevenue, on_delete=models.PROTECT, related_name='revenues')
    value = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    duedate = models.CharField(
        max_length=5,
        validators=[validate_day_month],
        help_text="Insira dia e mês DD-MM"
    )

    class Meta:
        ordering = ['name']

    def __str__(self): 
        return self.name 