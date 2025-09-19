from django.db import models
from revenues.models import Revenue



class Inflow(models.Model):
    #name = models.CharField(max_length=160)
    revenue  = models.ForeignKey(Revenue, on_delete=models.PROTECT, related_name='inflows')
    value = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    description = models.TextField(null=True, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.revenue)