from django.db import models
from invoices.models import Invoice
# Create your models here.

class InvoiceItem(models.Model):
    TYPE_CHOICES = [
        ('MONTHLY', 'Mensalidade'),
        ('COURSE', 'Curso'),
        ('EVENT', 'Evento'),
    ]

    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    item_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    due_date = models.DateField()

    def __str__(self):
        return f"{self.description} - R$ {self.amount}"
