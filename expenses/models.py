from django.db import models
from categories.models import Category
import datetime

def validate_day_month(value):
    """Valida se o valor está no formato correto de dia e mês."""
    try:
        datetime.datetime.strptime(value, "%d-%m")
    except ValueError:
        raise ValidationError("O valor deve estar no formato DD-MM (por exemplo, 25-12).")

class Expense(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, name='expenses')
    description = models.TextField(null=True, blank=True)
    value = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    duedate = models.CharField(max_length=5, validators=[validate_day_month], help_text="Insira dia e mês DD-MM")
    paid = models.BooleanField(default=True)

    class Meta:
        ordering = ['name'] 
    
    def __str__(self):
        return self.name 