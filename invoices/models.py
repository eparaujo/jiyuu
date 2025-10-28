from django.db import models
from karatecas.models import Karateca
from billingCycle.models import BillingCycle
from django.utils import timezone
from decimal import Decimal

class Invoice(models.Model):
    karateca = models.ForeignKey(Karateca, on_delete=models.CASCADE)
    billing_cycle = models.ForeignKey(BillingCycle, on_delete=models.CASCADE)
    due_date = models.DateField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('karateca', 'billing_cycle')

    def update_total(self):
        total = sum(item.amount for item in self.items.all())
        self.total_amount = Decimal(total)
        self.save()
 
    def mark_as_paid(self):
        self.paid = True
        self.paid_at = timezone.now()
        self.save()
