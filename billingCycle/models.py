from django.db import models

# Create your models here.
class BillingCycle(models.Model):
    month = models.PositiveSmallIntegerField()  # 1-12
    year = models.PositiveSmallIntegerField()
    closed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('month', 'year')

    def __str__(self):
        return f"{self.month:02d}/{self.year}"
